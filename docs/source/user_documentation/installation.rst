.. _installation:

Installation
============

Prerequisites
-------------

To build from source we recommend that you use **poetry**, however, this is **not needed** when just installing for your project.

.. code-block:: bash

   pip install poetry

Installation Process
--------------------

To install **ror** the process is simple, below select the most applicable approach for your project and follow the associated
instructions to install.

PIP Installation
^^^^^^^^^^^^^^^^
To install from the PyPI repository, run the following command.

.. code-block:: bash

   pip install ror

Build from Source
^^^^^^^^^^^^^^^^^

To build directly from source you can use the following commands.

.. code-block:: bash

   git clone https://github.com/PatrickTourniaire/ror.git && cd ror
   poetry install
   poetry build
   pip install ./dist/ror-<VERSION_CODE>-py3-none-any.whl
