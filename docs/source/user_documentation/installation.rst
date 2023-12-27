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

To install **pypipeline** the process is simple, below select the most applicable approach for your project and follow the associated
instructions to install.

PIP Installation
^^^^^^^^^^^^^^^^
To install from the PyPI repository, run the following command.

.. code-block:: bash

   pip install pypipeline

Build from Source
^^^^^^^^^^^^^^^^^

To build directly from source you can use the following commands.

.. code-block:: bash

   git clone https://github.com/PatrickTourniaire/pypipeline.git && cd pypipeline
   poetry install
   poetry build
   pip install ./dist/pypipeline-<VERSION_CODE>-py3-none-any.whl
