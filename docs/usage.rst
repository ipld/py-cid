=====
Usage
=====

Working with CIDv0
------------------

.. code-block:: python

    >>> from cid import make_cid, CIDv0
    >>> import multihash
    >>> import hashlib
    >>>
    >>> # you can use a base58-encoded hash to create a CIDv0
    >>> cid = make_cid('QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4')
    >>> cid.version
    0
    >>> cid.codec
    'dag-pb'

    >>> # or you can create a CIDv0 from a multihash directly
    >>> data = b"hello world"
    >>> digest = hashlib.sha256(data).digest()
    >>> mhash = multihash.encode(digest, "sha2-256")
    >>> cid = CIDv0(mhash)

    >>> # you can encode() a CID to get its string form for transmission
    >>> cid_str = cid.encode()
    >>> isinstance(cid_str, bytes)
    True

    >>> # you can use this string representation to create a CID object as well
    >>> make_cid(cid_str.decode())
    CIDv0(version=0, codec=dag-pb, multihash=b'\x12 \xb9M\'...')

    >>> # make_cid works with both str and bytes
    >>> make_cid(b'QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4')
    CIDv0(version=0, codec=dag-pb, multihash=b'\x12 \xb9M\'...')

Working with CIDv1
------------------

.. code-block:: python

    >>> from cid import make_cid, CIDv1
    >>> import multihash
    >>> import hashlib
    >>>
    >>> # you have to provide a multibase-encoded hash to create a CIDv1 object
    >>> cid = make_cid('zdj7WhuEjrB52m1BisYCtmjH1hSKa7yZ3jEZ9JcXaFRD51wVz')
    >>> cid.version
    1
    >>> cid.codec
    'dag-pb'

    >>> # or you can provide a multihash directly
    >>> data = b"hello world"
    >>> digest = hashlib.sha256(data).digest()
    >>> mhash = multihash.encode(digest, "sha2-256")
    >>> cid = CIDv1('dag-pb', mhash)
    >>> cid.version
    1

    >>> # you can encode the CID to get its string form
    >>> cid_str = cid.encode()
    >>> isinstance(cid_str, bytes)
    True

    >>> # CIDv1 also supports multiple encodings, with the help of `py-multibase` package
    >>> base64_encoded = cid.encode('base64')
    >>> isinstance(base64_encoded, bytes)
    True

    >>> # CIDv1 also supports make_cid with encoded CID strings
    >>> make_cid(base64_encoded.decode())
    CIDv1(version=1, codec=dag-pb, multihash=b'\x12 \xb9M\'...')


.. note::

    ``codec`` provided to ``make_cid`` should be a valid ``multicodec`` codec, supported by ``py-multicodec`` library.

    Different encodings for ``CIDv1().encode(encoding)`` is provided by ``py-multibase`` library.


Converting between versions
---------------------------

.. code-block:: python

    >>> from cid import CIDv0, CIDv1
    >>> import multihash
    >>> import hashlib
    >>>
    >>> # Create a CIDv0
    >>> data = b"hello world"
    >>> digest = hashlib.sha256(data).digest()
    >>> mhash = multihash.encode(digest, "sha2-256")
    >>> cidv0 = CIDv0(mhash)
    >>>
    >>> # you can convert a CIDv0 object to a CIDv1 object
    >>> cidv1 = cidv0.to_v1()
    >>> cidv1.version
    1
    >>> cidv1.codec
    'dag-pb'

    >>> # you can convert a CIDv1 object to a CIDv0 object as well
    >>> cidv1.to_v0().version
    0

.. warning::
    You can only convert a ``CIDv1`` object to ``CIDv0`` object if its codec is ``dag-pb``, otherwise conversion is not
    possible

    Likewise, when you convert a ``CIDv0`` object to ``CIDv1``, its codec will be set to ``dag-pb``

Equality across versions
------------------------

.. code-block:: python

    >>> from cid import CIDv0, CIDv1
    >>> import multihash
    >>> import hashlib
    >>>
    >>> # Create a CID with same multihash
    >>> data = b"hello world"
    >>> digest = hashlib.sha256(data).digest()
    >>> mhash = multihash.encode(digest, "sha2-256")
    >>> cidv0 = CIDv0(mhash)
    >>> cidv1 = CIDv1('dag-pb', mhash)
    >>>
    >>> # equality will only work across same versions, two CIDs are different if their versions are different
    >>> cidv0 == cidv1.to_v0()
    True
    >>> cidv0.to_v1() == cidv1
    True
    >>> cidv0 != cidv1
    True

JSON Marshaling (IPLD Format)
------------------------------

.. code-block:: python

    >>> from cid import CIDv0, CIDJSONEncoder
    >>> import json
    >>> import multihash
    >>> import hashlib
    >>>
    >>> # Create a CID
    >>> data = b"hello world"
    >>> digest = hashlib.sha256(data).digest()
    >>> mhash = multihash.encode(digest, "sha2-256")
    >>> cid = CIDv0(mhash)
    >>>
    >>> # Convert to IPLD JSON format
    >>> json_data = cid.to_json_dict()
    >>> json_data
    {'/': 'QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4'}
    >>>
    >>> # Parse from IPLD JSON format
    >>> restored = CIDv0.from_json_dict(json_data)
    >>> restored == cid
    True
    >>>
    >>> # Use with json.dumps()
    >>> json_str = json.dumps(cid, cls=CIDJSONEncoder)
    >>> json.loads(json_str)
    {'/': 'QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4'}

Prefix Operations
-----------------

.. code-block:: python

    >>> from cid import Prefix, CIDv0
    >>> import multihash
    >>> import hashlib
    >>>
    >>> # Create a prefix for CIDv0
    >>> prefix = Prefix.v0()
    >>> prefix.version, prefix.codec, prefix.mh_type
    (0, 'dag-pb', 'sha2-256')
    >>>
    >>> # Create a prefix for CIDv1
    >>> prefix_v1 = Prefix.v1(codec="raw", mh_type="sha2-256")
    >>> prefix_v1.version, prefix_v1.codec
    (1, 'raw')
    >>>
    >>> # Create CID from data using prefix
    >>> data = b"hello world"
    >>> cid = prefix.sum(data)
    >>> isinstance(cid, CIDv0)
    True
    >>>
    >>> # Extract prefix from existing CID
    >>> extracted_prefix = cid.prefix()
    >>> extracted_prefix.version, extracted_prefix.codec
    (0, 'dag-pb')
    >>>
    >>> # Serialize and deserialize prefix
    >>> prefix_bytes = prefix.to_bytes()
    >>> restored_prefix = Prefix.from_bytes(prefix_bytes)
    >>> restored_prefix == prefix
    True

/ipfs/ Path Parsing
--------------------

.. code-block:: python

    >>> from cid import from_string, parse_ipfs_path
    >>>
    >>> # Automatically extract CID from /ipfs/ paths
    >>> path = "/ipfs/QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4"
    >>> cid = from_string(path)
    >>> cid.version
    0
    >>>
    >>> # Works with URLs
    >>> url = "https://ipfs.io/ipfs/QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4"
    >>> cid = from_string(url)
    >>>
    >>> # Manual path parsing
    >>> cid_str = parse_ipfs_path("/ipfs/QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4")
    >>> cid_str
    'QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4'

Extract Encoding
----------------

.. code-block:: python

    >>> from cid import extract_encoding
    >>>
    >>> # Extract encoding from CIDv0
    >>> encoding = extract_encoding("QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4")
    >>> encoding
    'base58btc'
    >>>
    >>> # Extract encoding from CIDv1
    >>> encoding = extract_encoding("bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi")
    >>> encoding
    'base32'

Trailing Bytes Validation
--------------------------

.. code-block:: python

    >>> from cid import from_bytes_strict, CIDv1
    >>> import multihash
    >>> import hashlib
    >>>
    >>> # Create CIDv1
    >>> data = b"hello world"
    >>> digest = hashlib.sha256(data).digest()
    >>> mhash = multihash.encode(digest, "sha2-256")
    >>> cid = CIDv1("dag-pb", mhash)
    >>>
    >>> # Parse with strict validation (no trailing bytes)
    >>> cid_bytes = cid.buffer
    >>> parsed = from_bytes_strict(cid_bytes)
    >>> parsed == cid
    True
    >>>
    >>> # Raises error if trailing bytes present
    >>> from_bytes_strict(cid_bytes + b"extra")
    Traceback (most recent call last):
        ...
    ValueError: trailing bytes in CID data

Builder Pattern
---------------

.. code-block:: python

    >>> from cid import V0Builder, V1Builder
    >>>
    >>> # Create CIDv0 using builder
    >>> builder = V0Builder()
    >>> data = b"hello world"
    >>> cid = builder.sum(data)
    >>> cid.version
    0
    >>>
    >>> # Get codec
    >>> builder.get_codec()
    'dag-pb'
    >>>
    >>> # Create CIDv1 using builder
    >>> builder_v1 = V1Builder(codec="raw", mh_type="sha2-256")
    >>> cid = builder_v1.sum(data)
    >>> cid.version, cid.codec
    (1, 'raw')
    >>>
    >>> # Chain codec changes
    >>> new_builder = builder_v1.with_codec("dag-pb")
    >>> new_builder.get_codec()
    'dag-pb'

Set Operations
--------------

.. code-block:: python

    >>> from cid import CIDSet, CIDv0
    >>> import multihash
    >>> import hashlib
    >>>
    >>> # Create a set
    >>> cid_set = CIDSet()
    >>>
    >>> # Create some CIDs
    >>> data1 = b"hello"
    >>> data2 = b"world"
    >>> digest1 = hashlib.sha256(data1).digest()
    >>> digest2 = hashlib.sha256(data2).digest()
    >>> mhash1 = multihash.encode(digest1, "sha2-256")
    >>> mhash2 = multihash.encode(digest2, "sha2-256")
    >>> cid1 = CIDv0(mhash1)
    >>> cid2 = CIDv0(mhash2)
    >>>
    >>> # Add CIDs to set
    >>> cid_set.add(cid1)
    >>> cid_set.add(cid2)
    >>> len(cid_set)
    2
    >>>
    >>> # Check membership
    >>> cid_set.has(cid1)
    True
    >>> cid1 in cid_set
    True
    >>>
    >>> # Visit (add if new)
    >>> cid_set.visit(cid1)  # Already exists
    False
    >>> cid_set.visit(CIDv0(multihash.encode(hashlib.sha256(b"new").digest(), "sha2-256")))  # New
    True
    >>>
    >>> # Iterate over set
    >>> for cid in cid_set:
    ...     print(cid)
    QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4
    ...

Defined Check
-------------

.. code-block:: python

    >>> from cid import CIDv0
    >>> import multihash
    >>> import hashlib
    >>>
    >>> # Check if CID is defined
    >>> data = b"hello world"
    >>> digest = hashlib.sha256(data).digest()
    >>> mhash = multihash.encode(digest, "sha2-256")
    >>> cid = CIDv0(mhash)
    >>> cid.defined()
    True

Stream Parsing
--------------

.. code-block:: python

    >>> from cid import from_reader, CIDv1
    >>> import io
    >>> import multihash
    >>> import hashlib
    >>>
    >>> # Parse CID from stream/reader
    >>> data = b"hello world"
    >>> digest = hashlib.sha256(data).digest()
    >>> mhash = multihash.encode(digest, "sha2-256")
    >>> cid = CIDv1("dag-pb", mhash)
    >>> reader = io.BytesIO(cid.buffer)
    >>> bytes_read, parsed_cid = from_reader(reader)
    >>> parsed_cid == cid
    True
    >>> bytes_read == len(cid.buffer)
    True

Must Parse
----------

.. code-block:: python

    >>> from cid import must_parse
    >>>
    >>> # Parse CID, raises exception on error
    >>> cid = must_parse("QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4")
    >>> cid.version
    0
    >>>
    >>> # Raises ValueError for invalid CID
    >>> must_parse("invalid")
    Traceback (most recent call last):
        ...
    ValueError: Failed to parse CID: ...

Binary and Text Marshaling
---------------------------

.. code-block:: python

    >>> from cid import CIDv0
    >>> import multihash
    >>> import hashlib
    >>>
    >>> # Binary marshaling
    >>> data = b"hello world"
    >>> digest = hashlib.sha256(data).digest()
    >>> mhash = multihash.encode(digest, "sha2-256")
    >>> cid = CIDv0(mhash)
    >>>
    >>> # Get bytes representation
    >>> cid_bytes = cid.to_bytes()
    >>> cid_bytes == cid.buffer
    True
    >>>
    >>> # Text marshaling
    >>> text_bytes = cid.to_text()
    >>> isinstance(text_bytes, bytes)
    True
    >>>
    >>> # Parse from text
    >>> restored = CIDv0.from_text(text_bytes)
    >>> restored == cid
    True

Key String and Loggable
---------------------------

.. code-block:: python

    >>> from cid import CIDv0
    >>> import multihash
    >>> import hashlib
    >>>
    >>> # Get key string for use as dict key
    >>> data = b"hello world"
    >>> digest = hashlib.sha256(data).digest()
    >>> mhash = multihash.encode(digest, "sha2-256")
    >>> cid = CIDv0(mhash)
    >>>
    >>> key_str = cid.key_string()
    >>> isinstance(key_str, str)
    True
    >>>
    >>> # Get loggable dict
    >>> log_dict = cid.loggable()
    >>> log_dict
    {'cid': 'QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4'}
