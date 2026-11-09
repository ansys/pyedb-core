.. _contribute_pyedb:

Contribute
==========

Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <dev_guide_contributing_>`_ topic in the *PyAnsys developer's guide*.
Ensure that you are thoroughly familiar with this guide before attempting to contribute
to PyEDB-Core.

The following contribution information is specific to PyEDB-Core.

.. _dev_install:

Developer installation
----------------------
Installing the ``ansys-edb`` package in developer mode allows you to modify the source and
enhance it.

This package supports Python 3.9 through 3.12 on Windows, Linux, and MacOS.

#. Clone the repository:

   .. code:: bash

       git clone https://github.com/ansys/pyedb-core

#. Create a fresh-clean Python `virtual environment <venv_>`_ and activate it:

   .. code:: bash

       # Create a virtual environment
       python -m venv .venv

       # Activate it in a Linux environment
       source .venv/bin/activate

       # Activate it in a Windows CMD environment
       .venv\Scripts\activate.bat

       # Activate it in a Windows Powershell environment
       .venv\Scripts\Activate.ps1

#. Make sure you have the latest required build system and documentation, testing, and CI tools:

   .. code:: bash

       python -m pip install -U pip

       python -m pip install .[tests]

#. Verify your development installation:

   .. code:: bash

       tox

Testing
-------

This project takes advantage of `tox`_. Similar to Makefile, this tool allows you to automate
common tasks, but it is oriented towards Python development.

Using ``tox``
^^^^^^^^^^^^^

While Makefile has rules, `tox` has environments. In fact, the tool creates its
own virtual environment so anything being tested is isolated from the project
to guarantee the project's integrity. The following environments commands are provided:

- **tox -e style**: Checks for coding style quality.
- **tox -e test**: Checks for unit tests. Pass `pytest <pytest_>`_ flags after the
  ``--`` portion of the command. For example, use this ``pytest`` command to show the
  standard output, replacing ``X`` with the minor version of your Python environment:
  ``tox -e py3X -- -s``.
- **tox -e coverage**: Checks for code coverage.
- **tox -e doc**: Checks for documentation building.

Raw testing
^^^^^^^^^^^

If required, you can always call code style tools, such as `black`_, `isort`_,
and `flake8`_, or unit testing tools, such as `pytest`_ from the command line.
However, using these tools do not guarantee that your project is being tested in an isolated
environment, which is the reason why a tool like `tox`_ exists.

Adhere to code style
--------------------
PyEDB-Core follows the PEP8 standard as indicated in `PEP 8 <dev_guide_pyansys_pep8_>`_
in the *PyAnsys developer's guide*. It also implements style checking using `pre-commit <pre-commit_>`_.

To ensure your code meets minimum code styling standards, run these commands:

.. code:: console

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running this command:

.. code:: console

  pre-commit install

This way, it's not possible for you to push code that fails the code style checks:

.. code:: text

  $ git commit -am "added my cool feature"
  black....................................................................Passed
  blacken-docs.............................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  docformatter.............................................................Passed
  codespell................................................................Passed
  check for merge conflicts................................................Passed
  debug statements (python)................................................Passed
  check yaml...............................................................Passed
  trim trailing whitespace.................................................Passed
  Add License Headers......................................................Passed
  Validate GitHub Workflows................................................Passed

Documentation
-------------

To install the required dependencies for the documentation, run this command:

.. code::

    pip install .[doc]


To build the documentation, run the usual rules provided in the `Sphinx <Sphinx_>`_
Makefile for your operating system.

**On Windows:**

.. code::

   .\doc\make.bat html
   .\doc\build\html\index.html

**On Linux and MacOS:**

.. code::

   make -C doc/ html && your_browser_name doc/build/html/index.html

However, the recommended way of checking documentation integrity is to use ``tox``:

.. code:: bash

    tox -e doc && your_browser_name .tox/doc_out/html/index.html

Distributing
------------

If you would like to create either source or wheel files, run these commands:

.. code:: bash

        flit build
        python -m twine check dist/*

Boilerplate code generation
---------------------------

The pyedb-core API requires some boilerplate code for performance optimization (in particular,
the file `src/ansys/edb/core/inner/rpc_info.py`). This boilerplate code is dependent upon the proto files
used to create the `ansys-api-edb <ansys-api-edb_>`_ package. When changes are made to the proto files
in the `ansys-api-edb <ansys-api-edb_>`_ repository,the boilerplate code in the pyedb-core repository
must be synced with these changes. To do so, please run the `parse_protos.sh` script using the following command
(note that on windows, a git bash terminal should be used to run the shell script):

.. code:: bash

    cd ./scripts/proto_parser/
    ./parse_protos.sh

The `parse_protos.sh` script has the following requirements:

-  A local copy of the `ansys-api-edb <ansys-api-edb_>`_ repository
- The environment variable `ANSYS_API_EDB_REPO_PATH` set to the top level directory of your local `ansys-api-edb <ansys-api-edb_>`_ repository
- A python 3.10 installation accessible through the system library path environment variable (`Path` on Windows or `LD_LIBRARY_PATH` on Linux)

.. LINKS AND REFERENCES
.. _dev_guide_contributing: https://dev.docs.pyansys.com/how-to/contributing.html
.. _pyedb_repo: https://github.com/ansys/pyedb-core
.. _venv: https://docs.python.org/3/library/venv.html
.. _tox: https://tox.wiki/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _dynalib_repo_issues: https://github.com/ansys/pyedb-core/issues
.. _pytest: https://docs.pytest.org/en/stable/
.. _black: https://black.readthedocs.io/en/latest/
.. _isort: https://pycqa.github.io/isort/
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _dev_guide_pyansys_pep8: https://dev.docs.pyansys.com/coding-style/pep8.html
.. _pre-commit: https://pre-commit.com/
.. _ansys-api-edb: https://github.com/ansys/ansys-api-edb
