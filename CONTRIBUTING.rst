.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/ipld/py-cid/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

CID (Content IDentifier) could always use more documentation, whether as part of the
official CID (Content IDentifier) docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/ipld/py-cid/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `py-cid` for local development.

1. Fork the `py-cid` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/py-cid.git
    $ cd py-cid

3. Set up your development environment::

    # Create a virtual environment
    $ python3 -m venv ./venv

    # Activate the virtual environment
    $ source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install in development mode with all dependencies
    $ python3 -m pip install -e ".[dev]"

    # Install pre-commit hooks for code quality
    $ pre-commit install

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass all quality checks::

    # Run linting and formatting
    $ ruff check .
    $ ruff format .

    # Run type checking
    $ mypy cid/

    # Run tests
    $ pytest

    # Run all checks (linting, type checking, tests)
    $ make pr

   The pre-commit hooks will automatically run many of these checks when you commit.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.10+.
   Check the GitHub Actions CI and make sure that the tests pass for all supported Python versions.
4. All code should pass the pre-commit hooks (linting, formatting, type checking).
5. Use the `make pr` command to run all checks before submitting.

Development Tools
-----------------

The project uses modern development tools for code quality and testing:

**Code Quality:**
- `ruff` - Fast Python linter and formatter
- `mypy` - Static type checking
- `pre-commit` - Git hooks for automated checks

**Testing:**
- `pytest` - Test framework
- `pytest-cov` - Coverage reporting
- `hypothesis` - Property-based testing
- `tox` - Testing across multiple Python versions

**Documentation:**
- `sphinx` - Documentation generation
- `towncrier` - Changelog management

**Makefile Commands:**
- `make pr` - Run all checks (lint, typecheck, test)
- `make test` - Run tests with coverage
- `make lint` - Run linting
- `make typecheck` - Run type checking
- `make docs` - Generate documentation
- `make install-dev` - Install in development mode

Tips
----

To run a subset of tests::

    $ pytest tests/test_cid.py

To run specific test functions::

    $ pytest tests/test_cid.py::test_specific_function

To run tests with verbose output::

    $ pytest -v

To run linting only::

    $ ruff check .

To format code::

    $ ruff format .
