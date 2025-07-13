⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️

2022-09-15:

This repo is not maintained.

If someone would like to fork it and support it, IPLD stewards are happy to point to a supported fork.
Please open an issue in ipld/ipld requesting this of ask in #ipld in IPFS Discod, Matrix, or FIL Slack.

⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️


CID (Content IDentifier)
------------------------


.. image:: https://img.shields.io/pypi/v/py-cid.svg
        :target: https://pypi.python.org/pypi/py-cid

.. image:: https://img.shields.io/travis/ipld/py-cid.svg?branch=master
        :target: https://travis-ci.org/ipld/py-cid?branch=master

.. image:: https://codecov.io/gh/ipld/py-cid/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/ipld/py-cid

.. image:: https://readthedocs.org/projects/py-cid/badge/?version=stable
        :target: https://py-cid.readthedocs.io/en/stable/?badge=stable
        :alt: Documentation Status


What is CID ?
=============

`CID <https://github.com/ipld/cid>`_ is a format for referencing content in distributed information systems,
like `IPFS <https://ipfs.io>`_.
It leverages `content addressing <https://en.wikipedia.org/wiki/Content-addressable_storage>`_,
`cryptographic hashing <https://simple.wikipedia.org/wiki/Cryptographic_hash_function>`_, and
`self-describing formats <https://github.com/multiformats/multiformats>`_.

It is the core identifier used by `IPFS <https://ipfs.io>`_ and `IPLD <https://ipld.io>`_.

CID is a self-describing content-addressed identifier.

It uses cryptographic hashes to achieve content addressing.

It uses several `multiformats <https://github.com/multiformats/multiformats>`_ to achieve flexible self-description,
namely `multihash <https://github.com/multiformats/multihash>`_ for hashes,
`multicodec <https://github.com/multiformats/multicodec>`_ for data content
types, and `multibase <https://github.com/multiformats/multibase>`_ to encode the CID itself into strings.

Sample Usage
============

.. code-block:: python

    >>> from cid import make_cid
    >>> make_cid('QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4')
    CIDv0(version=0, codec=dag-pb, multihash=b"\x12 \xb9M'\xb9\x93M>\x08\xa5.R\xd7\xda}\xab\xfa\xc4\x84..")

    >>> cid = make_cid('QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4')
    >>> print(cid.version, cid.codec, cid.multihash)

    >>> print(cid.encode())
    QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4

    >>> str(cid)
    'QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4'




Other info
==========

* Free software: MIT license
* Documentation: https://py-cid.readthedocs.io.
* Python versions: 3.5, 3.6+
