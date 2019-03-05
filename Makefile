.PHONY: _help docs package test integration

_help:
	@echo "Please enter a valid make target from the list below:"
	@echo "docs - generate sphinx documentation"
	@echo "package - package up for pypi"
	@echo "test - run unit tests"
	@echo "integration - run integration tests"

docs:
	$(MAKE) -C docs html

package:
	python setup.py sdist bdist_wheel

test:
	coverage run -m unittest discover -s tests/relay_commander
	coverage html

integration:
	python -m unittest discover -s tests/integration
