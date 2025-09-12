py-cid v0.3.1 (2025-09-12)
--------------------------

Internal Changes - for py-cid Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The 0.3.0 release information is now in a newsfragment that can be processed by towncrier --version 0.3.0 to generate the changelog (`#40 <https://github.com/ipld/py-cid/issues/40>`__)


Miscellaneous Changes
~~~~~~~~~~~~~~~~~~~~~

- Complete build system modernization with pyproject.toml
  Added comprehensive development tooling (ruff, mypy, pre-commit, tox)
  Updated dependencies to use pymultihash instead of py-multihash
  Added GitHub Actions CI/CD pipeline
  Added type stubs for mypy support
  Updated Python version support to 3.10+
  Enhanced testing with pytest, hypothesis, and coverage
  Added towncrier for changelog management
  Improved documentation and contributing guidelines (`#40 <https://github.com/ipld/py-cid/issues/40>`__)


History
-------

0.2.1 (2018-10-20)
==================

* Fix edge cases with multibase and multihash decoding
* Added hypothesis tests while verifying CIDs

0.1.5 (2018-10-12)
==================

* Handle the case where an incorrect base58 encoded value is provided to `make_cid`

0.1.0 (2017-09-05)
==================

* First release on PyPI.
