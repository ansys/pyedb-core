PyEDB-Core
==========

|pyansys| |python| |pypi| |MIT|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-edb-core?logo=pypi
   :target: https://pypi.org/project/ansys-edb-core/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-edb-core.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-edb-core
   :alt: PyPI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

|GH-CI| |black|

.. |GH-CI| image:: https://github.com/ansys/pyedb-core/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/pyedb-core/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

.. reuse_start

PyEDB-Core is a Python client for the Electronics Database (EDB), a format for storing
information describing designs for Ansys Electronic Desktop (AEDT). Using the PyEDB-Core API,
you can make calls to an EDB server that is running either locally or remotely.

The EDB server can create, edit, read, and write EDB files to disk. These files can then be
read into AEDT and their designs simulated.

Documentation and issues
~~~~~~~~~~~~~~~~~~~~~~~~
Documentation for the latest stable release of PyEDB-Core is hosted at
`PyEDB-Core documentation <https://edb.core.docs.pyansys.com/version/stable/index.html#>`_.
The documentation has five sections:

- `Getting started <https://edb.core.docs.pyansys.com/version/stable/getting_started/index.html#>`_: Describes
  how to install PyEDB-Core in user mode.
- `User guide <https://edb.core.docs.pyansys.com/version/stable/user_guide/index.html>`_: Describes how to
  use PyEDB-Core.
- `API reference <https://edb.core.docs.pyansys.com/version/stable/api/index.html>`_: Provides API member descriptions
  and usage examples.
- `Examples <https://edb.core.docs.pyansys.com/version/stable/examples/index.html>`_: Provides examples showing
  end-to-end workflows for using PyEDB-Core.
- `Contribute <https://edb.core.docs.pyansys.com/version/stable/contribute.html>`_: Describes how to install
  PyEDB-Core in developer mode and how to contribute to this PyAnsys library.

In the upper right corner of the documentation's title bar, there is an option for switching from
viewing the documentation for the latest stable release to viewing the documentation for the
development version or previously released versions.

On the `PyEDB-Core Issues <https://github.com/ansys/pyedb-core/issues>`_ page, you can create
issues to report bugs and request new features. When possible, use these issue templates:

* Bug report template
* Feature request template
* Documentation issue template
* Example request template

If your issue does not fit into one of these categories, create your own issue.

On the `Discussions <https://discuss.ansys.com/>`_ page on the Ansys Developer portal, you can post questions,
share ideas, and get community feedback.

To reach the PyAnsys support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

License
~~~~~~~
PyEDB-Core is licensed under the MIT license.

PyEDB-Core makes no commercial claim over Ansys whatsoever. The use of this Python client requires
a legally licensed copy of AEDT. For more information, see the
`Ansys Electronics <https://www.ansys.com/products/electronics>`_ page on the Ansys website.
