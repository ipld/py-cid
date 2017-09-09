=====
Usage
=====

Working with CIDv0
------------------

.. code-block:: python

    >>> from cid import make_cid, CIDv0
    >>> # you can use a base58-encoded hash to create a CIDv0
    >>> make_cid('QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4')
    CIDv0(version=0, codec=dag-pb, multihash=b"\x12 \xb9M'..")

    >>> # or you can provide an encoded CID string to create a new object
    >>> cid = CIDv0('<base58 encoded hash>')

    >>> # you can encode() a CID to get its string form for transmission
    >>> cid.encode()
    b'FFkvz99YBscguy5gspNsvf'

    >>> # you can use this string representation to create a CID object as well
    >>> make_cid(cid.encode())
    CIDv0(version=0, codec=dag-pb, multihash=b'<base58 encoded hash>')

    >>> # make_cid works with both str and bytes
    >>> make_cid(b'QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4')
    CIDv0(version=0, codec=dag-pb, multihash=b"\x12 \xb9M'..")

Working with CIDv1
------------------

.. code-block:: python

    >>> from cid import make_cid, CIDv1
    >>> # you have to provide a multibase-encoded hash to create a CIDv1 object
    >>> make_cid('zdj7WhuEjrB52m1BisYCtmjH1hSKa7yZ3jEZ9JcXaFRD51wVz')
    CIDv1(version=1, codec=dag-pb, multihash=b"\x12 \xb9M'..")

    >>> # or you can provide a multihash directly
    >>> cid = CIDv1('dag-pb', '<multihash>')
    CIDv1(version=1, codec=dag-pb, multihash=b'<multihash>')

    >>> # you can encode the CID to get its string form
    >>> cid.encode()
    b'z7x3CtScH765HvShXT'

    >>> # CIDv1 also supports multiple encodings, with the help of `py-multibase` package
    >>> cid.encode('base64'), cid.encode('base8')
    (b'mBcDxtdWx0aWhhc2g+', b'7134036155352661643226414134664076')

    >>> # CIDv1 also supports make_cid with encoded CID strings
    >>> make_cid(cid.encode('base64'))
    CIDv1(version=1, codec=dag-pb, multihash=b'<multihash>')


.. note::

    ``codec`` provided to ``make_cid`` should be a valid ``multicodec`` codec, supported by ``py-multicodec`` library.

    Different encodings for ``CIDv1().encode(encoding)`` is provided by ``py-multibase`` library.


Converting between versions
---------------------------

.. code-block:: python

    >>> # you can convert a CIDv0 object to a CIDv1 object
    >>> CIDv0('<multihash>').to_v1()
    CIDv1(version=1, codec=dag-pb, multihash=b'<multihash>')

    >>> # you can convert a CIDv1 object to a CIDv0 object as well
    >>> CIDv1('dag-pb', '<multihash>').to_v0()
    CIDv0(version=0, codec=dag-pb, multihash=b'<some randome hash>')

.. warning::
    You can only convert a ``CIDv1`` object to ``CIDv0`` object if its codec is ``dag-pb``, otherwise conversion is not
    possible

    Likewise, when you convert a ``CIDv0`` object to ``CIDv1``, its codec will be set to ``dag-pb``

Equality across versions
------------------------

.. code-block:: python

    >>> # equality will only work across same versions, two CIDs are different if their versions are different
    >>> CIDv0('<multihash>') == CIDv1('dag-pb', '<multihash>').to_v0()
    True
    >>> CIDv0('<multihash>').to_v1() == CIDv1('dag-pb', '<multihash>')
    True
    >>> CIDv0('<multihash>') != CIDv1('dag-pb', '<multihash>')
    True
