"""Tests for CID Prefix operations."""

import hashlib

import pytest
import multihash

from cid import CIDv0, CIDv1, Prefix


@pytest.fixture
def test_data():
    return b"hello world"


@pytest.fixture
def test_hash():
    data = b"hello world"
    digest = hashlib.sha256(data).digest()
    return multihash.encode(digest, "sha2-256")


class TestPrefix:
    def test_init_v0(self):
        """Prefix.__init__: creates CIDv0 prefix correctly"""
        prefix = Prefix(version=0, codec="dag-pb", mh_type="sha2-256")
        assert prefix.version == 0
        assert prefix.codec == "dag-pb"
        assert prefix.mh_type == "sha2-256"
        assert prefix.mh_length == -1

    def test_init_v1(self):
        """Prefix.__init__: creates CIDv1 prefix correctly"""
        prefix = Prefix(version=1, codec="raw", mh_type="sha2-256", mh_length=32)
        assert prefix.version == 1
        assert prefix.codec == "raw"
        assert prefix.mh_type == "sha2-256"
        assert prefix.mh_length == 32

    def test_init_invalid_version(self):
        """Prefix.__init__: raises ValueError for invalid version"""
        with pytest.raises(ValueError, match="version must be 0 or 1"):
            Prefix(version=2, codec="dag-pb", mh_type="sha2-256")

    def test_init_v0_invalid_codec(self):
        """Prefix.__init__: raises ValueError for CIDv0 with non-dag-pb codec"""
        with pytest.raises(ValueError, match="CIDv0 can only use dag-pb codec"):
            Prefix(version=0, codec="raw", mh_type="sha2-256")

    def test_sum_v0(self, test_data):
        """Prefix.sum: creates CIDv0 from data"""
        prefix = Prefix.v0()
        cid = prefix.sum(test_data)
        assert isinstance(cid, CIDv0)
        assert cid.version == 0
        assert cid.codec == "dag-pb"

    def test_sum_v1(self, test_data):
        """Prefix.sum: creates CIDv1 from data"""
        prefix = Prefix.v1(codec="raw", mh_type="sha2-256")
        cid = prefix.sum(test_data)
        assert isinstance(cid, CIDv1)
        assert cid.version == 1
        assert cid.codec == "raw"

    def test_to_bytes_v0(self):
        """Prefix.to_bytes: serializes CIDv0 prefix"""
        prefix = Prefix.v0()
        prefix_bytes = prefix.to_bytes()
        assert isinstance(prefix_bytes, bytes)
        assert len(prefix_bytes) > 0

    def test_to_bytes_v1(self):
        """Prefix.to_bytes: serializes CIDv1 prefix"""
        prefix = Prefix.v1(codec="dag-pb", mh_type="sha2-256")
        prefix_bytes = prefix.to_bytes()
        assert isinstance(prefix_bytes, bytes)
        assert len(prefix_bytes) > 0

    def test_from_bytes_v0(self):
        """Prefix.from_bytes: deserializes CIDv0 prefix"""
        prefix = Prefix.v0()
        prefix_bytes = prefix.to_bytes()
        restored = Prefix.from_bytes(prefix_bytes)
        assert restored == prefix

    def test_from_bytes_v1(self):
        """Prefix.from_bytes: deserializes CIDv1 prefix"""
        prefix = Prefix.v1(codec="raw", mh_type="sha2-256", mh_length=32)
        prefix_bytes = prefix.to_bytes()
        restored = Prefix.from_bytes(prefix_bytes)
        assert restored == prefix

    def test_eq(self):
        """Prefix.__eq__: compares prefixes correctly"""
        prefix1 = Prefix.v0()
        prefix2 = Prefix.v0()
        prefix3 = Prefix.v1(codec="dag-pb", mh_type="sha2-256")

        assert prefix1 == prefix2
        assert prefix1 != prefix3

    def test_v0_factory(self):
        """Prefix.v0: creates CIDv0 prefix"""
        prefix = Prefix.v0()
        assert prefix.version == 0
        assert prefix.codec == "dag-pb"
        assert prefix.mh_type == "sha2-256"

    def test_v1_factory(self):
        """Prefix.v1: creates CIDv1 prefix"""
        prefix = Prefix.v1(codec="raw", mh_type="sha2-512")
        assert prefix.version == 1
        assert prefix.codec == "raw"
        assert prefix.mh_type == "sha2-512"


class TestCIDPrefix:
    """Tests for CID.prefix() method"""

    @pytest.fixture
    def test_hash(self):
        data = b"hello world"
        digest = hashlib.sha256(data).digest()
        return multihash.encode(digest, "sha2-256")

    def test_prefix_cidv0(self, test_hash):
        """BaseCID.prefix: extracts prefix from CIDv0"""
        cid = CIDv0(test_hash)
        prefix = cid.prefix()
        assert prefix.version == 0
        assert prefix.codec == "dag-pb"
        assert prefix.mh_type == "sha2-256"

    def test_prefix_cidv1(self, test_hash):
        """BaseCID.prefix: extracts prefix from CIDv1"""
        cid = CIDv1("raw", test_hash)
        prefix = cid.prefix()
        assert prefix.version == 1
        assert prefix.codec == "raw"
        assert prefix.mh_type == "sha2-256"

    def test_prefix_round_trip(self, test_hash):
        """BaseCID.prefix: round-trip prefix extraction and CID creation"""
        cid = CIDv1("dag-pb", test_hash)
        prefix = cid.prefix()
        # Can't easily round-trip without original data, but we can verify structure
        assert prefix.version == cid.version
        assert prefix.codec == cid.codec
