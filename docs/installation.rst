==============
Installation
==============

This guide covers different ways to install the py-cid package, from simple usage to full development setup.

Quick Install
=============

For basic usage, install the package directly from PyPI:

.. code-block:: bash

    pip install py-cid

This installs the latest stable version with all required dependencies.

Installation Methods
====================

From PyPI (Recommended)
-----------------------

For production use or when you want the latest stable release:

.. code-block:: bash

    pip install py-cid

From Source
-----------

If you want to install from the source code:

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/ipld/py-cid.git
    cd py-cid

    # Install in normal mode
    pip install .

Development Installation
========================

For development work, you'll want to install the package in editable mode so that changes to the source code are immediately reflected:

Development Install
-------------------

Install the package in development mode with all development dependencies:

.. code-block:: bash

    # Install in editable/development mode with dev dependencies
    pip install -e ".[dev]"

Or use the provided Makefile:

.. code-block:: bash

    make install-dev

Using the Makefile
==================

The project includes a Makefile with convenient commands:

.. code-block:: bash

    # Show all available commands
    make help

    # Install in development mode
    make install-dev

    # Install in normal mode
    make install

    # Run tests
    make test

    # Run linting
    make lint

    # Build distribution packages
    make dist

    # Generate documentation
    make docs

Troubleshooting
===============

Common Issues
-------------

**ImportError: No module named 'multihash'**
    Make sure you have installed all dependencies: `pip install -e ".[dev]"`

**Permission Errors**
    Use a virtual environment to avoid permission issues:
    
    .. code-block:: bash
    
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        pip install -e .

**Build Errors**
    Ensure you have the latest pip and setuptools:
    
    .. code-block:: bash
    
        pip install --upgrade pip setuptools wheel

Virtual Environment
===================

It's recommended to use a virtual environment for development:

.. code-block:: bash

    # Create a virtual environment
    python -m venv venv

    # Activate it (Linux/Mac)
    source venv/bin/activate

    # Activate it (Windows)
    venv\Scripts\activate

    # Install in development mode
    pip install -e .

    # Install in development mode with all dependencies
    pip install -e ".[dev]"

This isolates your project dependencies from your system Python installation. 