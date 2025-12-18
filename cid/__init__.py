"""Top-level package for CID (Content IDentifier)."""

__author__ = """Dhruv Baldawa"""
__email__ = "dhruv@dhruvb.com"
__version__ = "0.4.0"

from .cid import CIDv0, CIDv1, from_bytes, from_string, is_cid, make_cid  # noqa: F401
