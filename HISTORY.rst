History
=======

.. towncrier release notes start

py-cid v0.4.0 (2025-12-19)
--------------------------

Features
~~~~~~~~

- Add Python 3.14 to the supported and tested interpreter list across tox and CI. (`#45 <https://github.com/ipld/py-cid/issues/45>`__)
- Migrate from pymultihash to py-multihash >= 2.0.0 for better maintenance and modern API support. (`#47 <https://github.com/ipld/py-cid/issues/47>`__)


Internal Changes - for py-cid Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Update license format in pyproject.toml from deprecated TOML table to SPDX string format to comply with setuptools>=77.0.0 requirements. (`#46 <https://github.com/ipld/py-cid/issues/46>`__)
- Copied ``base58`` code directly into ``py-cid`` to avoid future dependency issues. (`#52 <https://github.com/ipld/py-cid/issues/52>`__)


py-cid v0.3.1 (2025-09-12)
--------------------------

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

0.2.1 (2018-10-20)
------------------

* Fix edge cases with multibase and multihash decoding
* Added hypothesis tests while verifying CIDs

0.1.5 (2018-10-12)
------------------

* Handle the case where an incorrect base58 encoded value is provided to `make_cid`

0.1.0 (2017-09-05)
------------------

* First release on PyPI.
