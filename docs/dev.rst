Developer Documentation
=======================

Installing Development Environment
----------------------------------

This project uses pipenv for dependency management. 

1. Make sure you have `pipenv <https://pipenv.readthedocs.io/en/latest/install/>`__ installed locally.
2. Clone this repo and run `pipenv install -e.`
3. Run some cli commands with `pipenv run rc`


Running Tests
-------------

Tests can be found in the ``tests`` directory. 

You can run tests with ``make tests``. 

If you want to run a specific test file you can do so with:

::

    python -m unittest tests/relay_commander/test$MODULE.py

Code Coverage
~~~~~~~~~~~~~

This project attempts to have 100% code coverage. when you run ``make test`` code coverage is automatically ran. You can view the code coverage report locally by opening up the index.html file in the ``htmlcov`` directory that gets created when you run ``make test``. 

Documentation
-------------

This project uses sphinx for documentation. You can generate the latest docs locally by running ``make docs``. You can then view them by opening up the ``index.html`` file in the ``docs/build/html`` directory. 

Linting and Style
-----------------

This project follows the `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ style guidelines. You can install ``pylint`` in order to ensure that all of your code is compliant with this standard. 


