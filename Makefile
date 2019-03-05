.PHONY: _help docs package test

_help:
	@echo "Please enter a valid make target from the list below:"
	@echo "package - package up for pypi"
	@echo "test - run tests"

docs:
	$(MAKE) -C docs html

package:
	python setup.py sdist bdist_wheel

test:
	coverage run -m unittest discover -s tests/relay_commander
	coverage html

integration:
	coverage run -m unittest discover -s tests/integration
