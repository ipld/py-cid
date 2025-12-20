"""CID Prefix operations for creating CIDs from data."""

import hashlib
from typing import TYPE_CHECKING

import multicodec
import multihash

if TYPE_CHECKING:
    from .cid import CIDv0, CIDv1


def _encode_varint(value: int) -> bytes:
    """
    Encode an integer as a varint.

    :param int value: The integer to encode
    :return: Varint-encoded bytes
    :rtype: bytes
    """
    if value < 0:
        msg = "Varint encoding only supports non-negative integers"
        raise ValueError(msg)

    result = bytearray()
    while value > 0x7F:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value & 0x7F)
    return bytes(result)


def _decode_varint(data: bytes, offset: int = 0) -> tuple[int, int]:
    """
    Decode a varint from bytes.

    :param bytes data: The bytes to decode from
    :param int offset: Starting offset in bytes
    :return: Tuple of (decoded value, bytes consumed)
    :rtype: tuple[int, int]
    :raises ValueError: if the varint is invalid
    """
    if offset >= len(data):
        msg = "Not enough data to decode varint"
        raise ValueError(msg)

    value = 0
    shift = 0
    bytes_consumed = 0

    for i in range(offset, len(data)):
        byte_val = data[i]
        value |= (byte_val & 0x7F) << shift
        bytes_consumed += 1

        if (byte_val & 0x80) == 0:
            break

        shift += 7
        if shift >= 64:  # Prevent overflow
            msg = "Varint too large"
            raise ValueError(msg)

    return value, bytes_consumed


class Prefix:
    """
    CID prefix metadata (version, codec, multihash type/length).

    Used to create CIDs from data by specifying the metadata and hashing the data.
    """

    def __init__(
        self,
        version: int,
        codec: str,
        mh_type: str,
        mh_length: int = -1,
    ) -> None:
        """
        Create a new Prefix.

        :param int version: CID version (0 or 1)
        :param str codec: Codec name (e.g., "dag-pb", "raw")
        :param str mh_type: Multihash type (e.g., "sha2-256", "sha2-512")
        :param int mh_length: Multihash length (-1 for default)
        :raises ValueError: if parameters are invalid
        """
        if version not in (0, 1):
            msg = "version must be 0 or 1"
            raise ValueError(msg)
        if version == 0 and codec != "dag-pb":
            msg = "CIDv0 can only use dag-pb codec"
            raise ValueError(msg)
        if not multicodec.is_codec(codec):
            msg = f"invalid codec {codec!r}"
            raise ValueError(msg)

        self.version = version
        self.codec = codec
        self.mh_type = mh_type
        self.mh_length = mh_length

    def sum(self, data: bytes) -> "CIDv0 | CIDv1":
        """
        Hash data and create CID from resulting multihash.

        :param bytes data: The data to hash
        :return: CID object
        :rtype: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
        :raises NotImplementedError: if hash type is not supported
        """
        # Hash data using mh_type
        if self.mh_type == "sha2-256":
            digest = hashlib.sha256(data).digest()
        elif self.mh_type == "sha2-512":
            digest = hashlib.sha512(data).digest()
        else:
            # Use multihash library for other types
            # This is a simplified implementation - in practice,
            # you'd want to support more hash types
            msg = f"Hash type {self.mh_type} not fully implemented"
            raise NotImplementedError(msg)

        # Encode as multihash
        # Pass None if mh_length is -1 (default), otherwise use specified length
        mh_length = None if self.mh_length == -1 else self.mh_length
        mhash = multihash.encode(digest, self.mh_type, mh_length)

        # Create CID
        if self.version == 0:
            from .cid import CIDv0

            return CIDv0(mhash)
        else:
            from .cid import CIDv1

            return CIDv1(self.codec, mhash)

    def to_bytes(self) -> bytes:
        """
        Serialize prefix to bytes.

        Format: <version><codec-varint><mh-type-varint><mh-length-varint>

        :return: Serialized prefix bytes
        :rtype: bytes
        """
        # Version is a single byte (0 or 1)
        version_bytes = bytes([self.version])

        # Get codec prefix (already varint-encoded)
        codec_prefix = multicodec.get_prefix(self.codec)
        # Decode to get code, then re-encode (to ensure consistency)
        codec_code, _ = _decode_varint(codec_prefix, 0)
        codec_bytes = _encode_varint(codec_code)

        # Get multihash type code as integer
        # Note: multihash library uses string names, we need to map to codes
        mh_type_code = self._mh_type_to_code(self.mh_type)
        mh_type_bytes = _encode_varint(mh_type_code)

        # Multihash length
        mh_length_bytes = _encode_varint(self.mh_length if self.mh_length >= 0 else 0)

        return version_bytes + codec_bytes + mh_type_bytes + mh_length_bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> "Prefix":
        """
        Deserialize prefix from bytes.

        :param bytes data: Serialized prefix bytes
        :return: Prefix object
        :rtype: :py:class:`cid.prefix.Prefix`
        :raises ValueError: if the data is invalid
        """
        if len(data) < 1:
            msg = "Not enough data to decode prefix"
            raise ValueError(msg)

        offset = 0

        # Version (1 byte)
        version = int(data[offset])
        offset += 1

        if version not in (0, 1):
            msg = f"Invalid version: {version}"
            raise ValueError(msg)

        # Codec (varint)
        codec_code, bytes_consumed = _decode_varint(data, offset)
        offset += bytes_consumed
        # Reconstruct codec prefix bytes to use with multicodec
        codec_prefix = _encode_varint(codec_code)
        codec = multicodec.get_codec(codec_prefix)
        if not codec:
            msg = f"Unknown codec code: {codec_code}"
            raise ValueError(msg)

        # Multihash type (varint)
        mh_type_code, bytes_consumed = _decode_varint(data, offset)
        offset += bytes_consumed
        mh_type = cls._mh_code_to_type(mh_type_code)

        # Multihash length (varint)
        mh_length, bytes_consumed = _decode_varint(data, offset)
        if mh_length == 0:
            mh_length = -1

        return cls(version, codec, mh_type, mh_length)

    @staticmethod
    def _mh_type_to_code(mh_type: str) -> int:
        """Convert multihash type name to code."""
        # Common multihash type codes
        # These match the multiformats specification
        mh_codes = {
            "sha1": 0x11,
            "sha2-256": 0x12,
            "sha2-512": 0x13,
            "sha3-224": 0x17,
            "sha3-256": 0x16,
            "sha3-512": 0x14,
            "blake2b-256": 0xB220,
            "blake2b-512": 0xB240,
        }
        if mh_type not in mh_codes:
            msg = f"Unknown multihash type: {mh_type}"
            raise ValueError(msg)
        return mh_codes[mh_type]

    @staticmethod
    def _mh_code_to_type(mh_code: int) -> str:
        """Convert multihash code to type name."""
        mh_types = {
            0x11: "sha1",
            0x12: "sha2-256",
            0x13: "sha2-512",
            0x17: "sha3-224",
            0x16: "sha3-256",
            0x14: "sha3-512",
            0xB220: "blake2b-256",
            0xB240: "blake2b-512",
        }
        if mh_code not in mh_types:
            msg = f"Unknown multihash code: {mh_code}"
            raise ValueError(msg)
        return mh_types[mh_code]

    def __eq__(self, other: object) -> bool:
        """Check equality with another Prefix."""
        if not isinstance(other, Prefix):
            return False
        return (
            self.version == other.version
            and self.codec == other.codec
            and self.mh_type == other.mh_type
            and self.mh_length == other.mh_length
        )

    def __repr__(self) -> str:
        """String representation of Prefix."""
        return (
            f"Prefix(version={self.version}, codec={self.codec!r}, "
            f"mh_type={self.mh_type!r}, mh_length={self.mh_length})"
        )

    @classmethod
    def v0(cls) -> "Prefix":
        """
        Create a CIDv0 prefix.

        :return: Prefix for CIDv0
        :rtype: :py:class:`cid.prefix.Prefix`
        """
        return cls(version=0, codec="dag-pb", mh_type="sha2-256", mh_length=-1)

    @classmethod
    def v1(cls, codec: str, mh_type: str, mh_length: int = -1) -> "Prefix":
        """
        Create a CIDv1 prefix.

        :param str codec: Codec name
        :param str mh_type: Multihash type
        :param int mh_length: Multihash length (-1 for default)
        :return: Prefix for CIDv1
        :rtype: :py:class:`cid.prefix.Prefix`
        """
        return cls(version=1, codec=codec, mh_type=mh_type, mh_length=mh_length)
