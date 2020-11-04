#!/usr/bin/env python3

import argparse
import json

from .processor import process_from_files


def main():
    parser = argparse.ArgumentParser(
        description='jose5, task definition generator for ECS')
    parser.add_argument('filename', nargs='+', help='Templates')

    args = parser.parse_args()

    td = process_from_files(args.filename)
    print(json.dumps(td, indent=2))


if __name__ == "__main__":
    main()
