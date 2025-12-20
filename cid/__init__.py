"""Top-level package for CID (Content IDentifier)."""

__author__ = """Dhruv Baldawa"""
__email__ = "dhruv@dhruvb.com"
__version__ = "0.4.0"

from .cid import (  # noqa: F401
    CIDJSONEncoder,
    CIDv0,
    CIDv1,
    extract_encoding,
    from_bytes,
    from_bytes_strict,
    from_reader,
    from_string,
    is_cid,
    make_cid,
    must_parse,
    parse_ipfs_path,
)
from .builder import Builder, V0Builder, V1Builder  # noqa: F401
from .prefix import Prefix  # noqa: F401
from .set import CIDSet  # noqa: F401
