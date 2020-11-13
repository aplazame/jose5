#!make

dist: jose5/*.py
	python3 setup.py sdist bdist_wheel

publish: dist
	python3 -m twine upload dist/*
