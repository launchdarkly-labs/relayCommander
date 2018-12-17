.PHONY: _help package test

_help:
	@echo "Please enter a valid make target from the list below:"
	@echo "package - package up for pypi"
	@echo "test - run tests"

package:
	python setup.py sdist bdist_wheel

test:
	coverage run -m unittest discover
	coverage html