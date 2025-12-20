API Reference
=============

Helper functions
~~~~~~~~~~~~~~~~

.. py:currentmodule:: cid

.. autofunction:: make_cid

.. autofunction:: is_cid

.. autofunction:: from_string

.. autofunction:: from_bytes

.. autofunction:: from_bytes_strict

.. autofunction:: from_reader

.. autofunction:: must_parse

.. autofunction:: parse_ipfs_path

.. autofunction:: extract_encoding

CID classes
~~~~~~~~~~~

.. autoclass:: CIDv0
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:

.. autoclass:: CIDv1
    :show-inheritance:
    :members:
    :inherited-members:
    :undoc-members:

.. autoclass:: CIDJSONEncoder
    :show-inheritance:
    :members:

Prefix operations
~~~~~~~~~~~~~~~~~

.. autoclass:: cid.prefix.Prefix
    :no-index:
    :members:
    :show-inheritance:

Builder pattern
~~~~~~~~~~~~~~~

.. autoclass:: cid.builder.Builder
    :no-index:
    :members:
    :show-inheritance:

.. autoclass:: cid.builder.V0Builder
    :no-index:
    :members:
    :show-inheritance:

.. autoclass:: cid.builder.V1Builder
    :no-index:
    :members:
    :show-inheritance:

Set operations
~~~~~~~~~~~~~~

.. autoclass:: cid.set.CIDSet
    :no-index:
    :members:
    :show-inheritance:
