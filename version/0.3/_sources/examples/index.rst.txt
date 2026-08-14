Examples
========

Examples in the form of Jupyter notebooks demonstrate API usage.
To run these notebooks, perform these steps:

#. Create and activate a Python `virtual environment <venv_>`_:

   .. code:: bash

       python -m venv .venv
       .venv\Scripts\activate.bat

    For more information on creating and installing a virtual environment, see
    :ref:`dev_install`.

#. Ensure that you have the latest version of `pip`_:

   .. code:: bash

       python -m pip install -U pip

#. Build and install the ``ansys-edb`` and ``ansys-api`` packages:

   .. code:: bash

       python -m pip install -e .

#. Install Jupyter notebook requirements:

   .. code:: bash

       python -m pip install .[notebook]

#. Install the IPython kernel:

   .. code:: bash

       ipython kernel install --user --name=.venv

#. Launch Juptyer notebook:

   .. code:: bash

       jupyter-notebook

6. Navigate to desired notebook example, change the kernel to the virtual environment, and execute the notebook
   with the desired settings.

.. LINKS AND REFERENCES
.. _venv: https://docs.python.org/3/library/venv.html
.. _pip: https://pypi.org/project/pip/
