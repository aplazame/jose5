import json
import os
import re
from copy import deepcopy
from pathlib import Path


def valmap(M, map_fn):
    if isinstance(M, dict):
        return {key: valmap(x, map_fn) for key, x in M.items()}
    elif isinstance(M, list):
        return [valmap(x, map_fn) for x in M]
    else:
        return map_fn(M)


varre = re.compile('\$\{[A-Za-z0-9_\.]*\}')


def varsubst(V, s):
    if isinstance(s, str):
        for match in varre.findall(s):
            varpath = match[2:-1]

            vartoks = varpath.split('.')
            Vptr = V

            while vartoks:
                vartok = vartoks.pop(0)

                if isinstance(Vptr, dict) and vartok in Vptr:
                    Vptr = Vptr[vartok]
                else:
                    vartoks.insert(0, vartok)
                    break

            if not vartoks:
                if isinstance(Vptr, str):
                    s = s.replace(match, Vptr)

                if isinstance(Vptr, int) or isinstance(Vptr, float):
                    if match == s:
                        s = Vptr
                    else:
                        s = s.replace(match, str(Vptr))

    return s


def name(obj):
    if isinstance(obj, dict):
        return obj.get('name')
    elif isinstance(obj, str):
        return obj

    return None


def merge(A, B):
    if not A:
        return B

    if isinstance(B, dict):
        R = deepcopy(A)
        for key, value in B.items():
            R[key] = merge(A.get(key), value)
        pass
        return R
    elif isinstance(B, list):
        R = [x for x in A + B if not name(x)]

        Anamed = {name(x): x for x in A if name(x)}
        Bnamed = {name(x): x for x in B if name(x)}

        M = merge(Anamed, Bnamed)

        R = R + [val for val in M.values()]

        return R
    else:
        return B


def compose_file(path):
    with open(path) as f:
        templ = json.load(f)

    if '__extends' in templ:
        relpath = templ['__extends']
        subpath = (path.parent / Path(relpath)).resolve()
        templ = merge(compose_file(subpath), templ)

    return templ


def compose_from_paths(paths):
    R = compose_file(paths[0])

    for path in paths[1:]:
        R = merge(R, compose_file(path))

    return R


def process_templ(templ):
    prev_var_closure = {}
    var_closure = templ.get('__variables', {})

    var_closure = merge(dict(os.environ), var_closure)

    while prev_var_closure != var_closure:
        prev_var_closure, var_closure = var_closure, valmap(
            var_closure, lambda val: varsubst(var_closure, val))

    varvals = var_closure

    td = valmap(templ, lambda val: varsubst(varvals, val))

    if '__extends' in td:
        del td['__extends']

    if '__variables' in td:
        del td['__variables']

    return td


def process_from_files(filenames):
    templ = compose_from_paths(list(map(Path, filenames)))
    td = process_templ(templ)

    return td
