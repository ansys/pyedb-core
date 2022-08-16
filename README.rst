Pyedb
=====

Ansys Electronics Database Python Client

.. image:: https://github.com/pyansys/pyedb/actions/workflows/ci_cd.yml/badge.svg?branch=develop

How to install
--------------

At least two installation modes are provided: user and developer.

[NOT RELEASED] For users
^^^^^^^^^^^^^^^^^^^^^^^^

<This instruction does not work until this package is released to PyPI. Go to "For developers" section instead.>

In order to install Pyedb, make sure you
have the required build system tool. To do so, run:

.. code:: bash

    python -m pip install -U pip

Then, you can simply execute:

.. code:: bash

    python -m pip install ansys-edb

For developers
^^^^^^^^^^^^^^

Installing Pyedb in developer mode allows
you to modify the source and enhance it.

Before contributing to the project, please refer to the `PyAnsys Developer's guide`_. You will 
need to follow these steps:

1. Start by cloning this repository:

    .. code:: bash

        git clone https://github.com/pyansys/pyedb
        cd pyedb

2. Create a fresh-clean Python environment and activate it:

    .. code:: bash

        # Create a virtual environment
        python -m venv .venv

        # Activate it in a Linux environment
        python -m venv .venv && source .venv/bin/activate

        # Activate it in a Windows CMD environment
        .venv\Scripts\activate.bat

        # Activate it in a Windows Powershell environment
        .venv\Scripts\Activate.ps1


3. Make sure you have the latest required build system and doc, testing, and CI tools:

    .. code:: bash

        python -m pip install -U pip tox

        # Copy default environment variables for test
        cp .env.test.example .env.test

        # Modify .env.test if necessary


4. Finally, verify your development installation by running:

    .. code:: bash
        
        tox


How to testing
--------------

This project takes advantage of `tox`_. This tool allows to automate common
development tasks (similar to Makefile) but it is oriented towards Python
development. 

Using tox
^^^^^^^^^

As Makefile has rules, `tox`_ has environments. In fact, the tool creates its
own virtual environment so anything being tested is isolated from the project in
order to guarantee project's integrity. The following environments commands are provided:

- **tox -e style**: will check for coding style quality.
- **tox -e test**: checks for unit tests. Replace X with the minor version of your Python environment. Pass pytest flags after "--". For example, `tox -e py3X -- -s` to show stdout from pytest
- **tox -e coverage**: checks for code coverage.
- **tox -e doc**: checks for documentation building process.


Raw testing
^^^^^^^^^^^

If required, you can always call the style commands (`black`_, `isort`_,
`flake8`_...) or unit testing ones (`pytest`_) from the command line. However,
this does not guarantee that your project is being tested in an isolated
environment, which is the reason why tools like `tox`_ exist.


A note on pre-commit
^^^^^^^^^^^^^^^^^^^^

The style checks take advantage of `pre-commit`_. Developers are not forced but
encouraged to install this tool via:

.. code:: bash

    python -m pip install pre-commit && pre-commit install


Documentation
-------------

For building documentation, you can either run the usual rules provided in the
`Sphinx`_ Makefile, such us:

.. code:: bash

    make -C doc/ html && your_browser_name doc/html/index.html

However, the recommended way of checking documentation integrity is using:

.. code:: bash

    tox -e doc && your_browser_name .tox/doc_out/html/index.html


Distributing
------------

If you would like to create either source or wheel files, start by installing
the building requirements:

.. code:: bash

    python -m pip install -r requirements/requirements_build.txt

Then, you can execute:

.. code:: bash

        flit build
        python -m twine check dist/*

.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _pre-commit: https://pre-commit.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _tox: https://tox.wiki/
