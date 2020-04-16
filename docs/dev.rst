Developer Documentation
=======================

Installing Development Environment
----------------------------------

This project uses pip for dependency management. You'll have a better time if
you use a `virtualenv <https://docs.python.org/3/library/venv.html>`__.

1. Create a new virtualenv with ``python -m venv venv``.
2. Activate the new virtualenv with ``. venv/bin/activate``.
3. Install all of the project dependencies with
   ``pip install -r dev-requirements.txt``.
4. Install relayCommander in editable form with ``pip install -e .``
5. Try out some cli commands with ``rc``.


Running Tests
-------------

Tests can be found in the ``tests`` directory.

You can run tests with ``make test``.

If you want to run a specific test file you can do so with:

::

    python -m unittest tests/relay_commander/test$MODULE.py

Code Coverage
~~~~~~~~~~~~~

This project attempts to have 100% code coverage. when you run ``make test``
code coverage is automatically ran. You can view the code coverage report
locally by opening up the index.html file in the ``htmlcov`` directory
that gets created when you run ``make test``.

Documentation
-------------

This project uses sphinx for documentation. You can generate the latest docs
locally by running ``make docs``. You can then view them by opening up the
``index.html`` file in the ``docs/build/html`` directory.

Linting and Style
-----------------

This project follows the `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ style guidelines. You can install ``pylint`` in order to ensure that all of your code is compliant with this standard.

Release Checklist
-----------------

* update VERSION in version.py
* make sure CHANGELOG has release date and relevant changes
* git tag with the new version (make sure it matches version.py)
