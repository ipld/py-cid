import json
import re
from typing import TYPE_CHECKING, Any, cast

from morphys import ensure_bytes, ensure_unicode
import multibase
import multicodec
import multihash as mh

from . import base58

if TYPE_CHECKING:
    from .prefix import Prefix


class BaseCID:
    def __hash__(self) -> int:
        """Make CID hashable for use in sets and dicts."""
        return hash((self.version, self.codec, self.multihash))

    def __init__(self, version: int, codec: str, multihash: str | bytes) -> None:
        """
        Creates a new CID object. This class should not be used directly, use
        :py:class:`cid.cid.CIDv0` or :py:class:`cid.cid.CIDv1` instead.


        :param int version: CID version (0 or 1)
        :param str codec: codec to be used for encoding the hash
        :param str multihash: the multihash
        """
        self._version = version
        self._codec = codec
        self._multihash = ensure_bytes(multihash)

    @property
    def version(self) -> int:
        """CID version"""
        return self._version

    @property
    def codec(self) -> str:
        """CID codec"""
        return self._codec

    @property
    def multihash(self) -> bytes:
        """CID multihash"""
        return self._multihash

    @property
    def buffer(self) -> bytes:
        raise NotImplementedError

    def encode(self, encoding: str | None = None) -> bytes:  # noqa: ARG002
        raise NotImplementedError

    def __repr__(self) -> str:
        def truncate(s: bytes, length: int) -> bytes:
            return s[:length] + b".." if len(s) > length else s

        truncate_length = 20
        return (
            f"{self.__class__.__name__}(version={self._version}, "
            f"codec={self._codec}, multihash={truncate(self._multihash, truncate_length)!r})"
        )

    def __str__(self) -> str:
        return ensure_unicode(self.encode())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseCID):
            return False
        return (
            (self.version == other.version)
            and (self.codec == other.codec)
            and (self.multihash == other.multihash)
        )

    def to_json_dict(self) -> dict[str, str]:
        """
        Convert CID to IPLD JSON format.

        Returns a dictionary in IPLD JSON format: {"/": "<cid-string>"}

        :return: IPLD JSON format dictionary
        :rtype: dict
        """
        return {"/": str(self)}

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "CIDv0 | CIDv1":
        """
        Parse CID from IPLD JSON format.

        :param dict data: IPLD JSON format dictionary with "/" key
        :return: CID object
        :rtype: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
        :raises ValueError: if the format is invalid
        """
        if not isinstance(data, dict):
            msg = "Invalid IPLD JSON format: expected dict"
            raise ValueError(msg)
        if "/" not in data:
            msg = 'Invalid IPLD JSON format: missing "/" key'
            raise ValueError(msg)
        return from_string(str(data["/"]))

    def defined(self) -> bool:
        """
        Check if CID is defined (valid).

        :return: True if CID is defined, False otherwise
        :rtype: bool
        """
        return self.multihash is not None and len(self.multihash) > 0

    def to_bytes(self) -> bytes:
        """
        Serialize to bytes (alias for buffer).

        :return: Raw CID bytes
        :rtype: bytes
        """
        return self.buffer

    def to_text(self) -> bytes:
        """
        Serialize to text.

        :return: Encoded CID string as bytes
        :rtype: bytes
        """
        return str(self).encode()

    @classmethod
    def from_text(cls, text: bytes) -> "CIDv0 | CIDv1":
        """
        Deserialize from text.

        :param bytes text: Encoded CID string
        :return: CID object
        :rtype: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
        """
        return from_string(text.decode())

    def key_string(self) -> str:
        """
        Return binary representation as string for use as map keys.

        :return: Binary representation as string
        :rtype: str
        """
        return self.buffer.decode("latin-1")

    def loggable(self) -> dict[str, str]:
        """
        Return dict for logging purposes.

        :return: Dictionary with CID information
        :rtype: dict
        """
        return {"cid": str(self)}

    def prefix(self) -> "Prefix":
        """
        Get prefix from CID.

        Extracts the prefix metadata (version, codec, multihash type/length) from the CID.

        :return: Prefix object
        :rtype: :py:class:`cid.prefix.Prefix`
        """
        from .prefix import Prefix

        # Decode multihash to get type and length
        mh_info = mh.decode(self.multihash)
        # mh_info has name, code, length, digest attributes
        mh_type = mh_info.name
        mh_length = mh_info.length

        return Prefix(
            version=self.version,
            codec=self.codec,
            mh_type=mh_type,
            mh_length=mh_length,
        )


class CIDv0(BaseCID):
    """CID version 0 object"""

    CODEC = "dag-pb"

    def __init__(self, multihash: str | bytes) -> None:
        """
        :param bytes multihash: multihash for the CID
        """
        super().__init__(0, self.CODEC, multihash)

    @property
    def buffer(self) -> bytes:
        """
        The raw representation that will be encoded.

        :return: the multihash
        :rtype: bytes
        """
        return self.multihash

    def encode(self, encoding: str | None = None) -> bytes:  # noqa: ARG002
        """
        base58-encoded buffer

        :return: encoded representation or CID
        :rtype: bytes
        """
        return ensure_bytes(base58.b58encode(self.buffer))

    def to_v1(self) -> "CIDv1":
        """
        Get an equivalent :py:class:`cid.CIDv1` object.

        :return: :py:class:`cid.CIDv1` object
        :rtype: :py:class:`cid.CIDv1`
        """
        return CIDv1(self.CODEC, self.multihash)


class CIDv1(BaseCID):
    """CID version 1 object"""

    def __init__(self, codec: str, multihash: str | bytes) -> None:
        super().__init__(1, codec, multihash)

    @property
    def buffer(self) -> bytes:
        """
        The raw representation of the CID

        :return: raw representation of the CID
        :rtype: bytes
        """
        return b"".join([bytes([self.version]), multicodec.add_prefix(self.codec, self.multihash)])

    def encode(self, encoding: str | None = "base58btc") -> bytes:
        """
        Encoded version of the raw representation

        :param str encoding: the encoding to use to encode the raw representation,
            should be supported by ``py-multibase``
        :return: encoded raw representation with the given encoding
        :rtype: bytes
        """
        return multibase.encode(encoding, self.buffer)

    def to_v0(self) -> CIDv0:
        """
        Get an equivalent :py:class:`cid.CIDv0` object.

        :return: :py:class:`cid.CIDv0` object
        :rtype: :py:class:`cid.CIDv0`
        :raise ValueError: if the codec is not 'dag-pb'
        """
        if self.codec != CIDv0.CODEC:
            msg = f"CIDv1 can only be converted for codec {CIDv0.CODEC}"
            raise ValueError(msg)

        return CIDv0(self.multihash)


def make_cid(*args: str | bytes | int) -> CIDv0 | CIDv1:
    """
    Creates a :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1` object based on the given parameters

    The function supports the following signatures:

            make_cid(<base58 encoded multihash CID>) -> CIDv0

            make_cid(<multihash CID>) -> CIDv0

            make_cid(<multibase encoded multihash CID>) -> CIDv1

            make_cid(<version>, <codec>, <multihash>) -> CIDv1

    :param args:
        - base58-encoded multihash (str or bytes)
        - multihash (str or bytes)
        - multibase-encoded multihash (str or bytes)
        - version:int, codec(str), multihash(str or bytes)
    :returns: the respective CID object
    :rtype: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
    :raises ValueError: if the number of arguments is not 1 or 3
    :raises ValueError: if the only argument passed is not a ``str`` or a ``byte``
    :raises ValueError: if the string provided is not a valid base58 encoded hash
    :raises ValueError: if 3 arguments are passed and version is not 0 or 1
    :raises ValueError: if 3 arguments are passed and the ``codec`` is not
        supported by ``multicodec``
    :raises ValueError: if 3 arguments are passed and the ``multihash`` is not ``str`` or ``byte``
    :raises ValueError: if 3 arguments are passed with version 0 and codec is not *dag-pb*
    """
    if len(args) == 1:
        data = args[0]
        if isinstance(data, str):
            return from_string(data)
        if isinstance(data, bytes):
            return from_bytes(data)
        msg = f"invalid argument passed, expected: str or byte, found: {type(data)}"
        raise ValueError(msg)

    if len(args) == 3:
        version, codec, multihash = args
        if version not in (0, 1):
            msg = f"version should be 0 or 1, {version!r} was provided"
            raise ValueError(msg)
        if not isinstance(codec, str):
            msg = "codec must be a string"
            raise ValueError(msg)
        if not multicodec.is_codec(codec):
            msg = f"invalid codec {codec!r} provided, please check"
            raise ValueError(msg)
        if not isinstance(multihash, (str, bytes)):
            msg = "invalid type for multihash provided, should be str or bytes"
            raise ValueError(msg)

        if version == 0:
            if codec != CIDv0.CODEC:
                msg = f"codec for version 0 can only be {CIDv0.CODEC}, found: {codec}"
                raise ValueError(msg)
            return CIDv0(multihash)
        return CIDv1(codec, multihash)
    msg = "invalid number of arguments, expected 1 or 3"
    raise ValueError(msg)


def is_cid(cidstr: str | bytes) -> bool:
    """
    Checks if a given input string is valid encoded CID or not.
    It takes same input as `cid.make_cid` method with a single argument


    :param cidstr: input string which can be a

        - base58-encoded multihash
        - multihash
        - multibase-encoded multihash
    :type cidstr: str or bytes
    :return: if the value is a valid CID or not
    :rtype: bool
    """
    try:
        return bool(make_cid(cidstr))
    except ValueError:
        return False


def parse_ipfs_path(path: str) -> str:
    """
    Extract CID from /ipfs/ path.

    Handles various formats:
    - /ipfs/Qm...
    - https://ipfs.io/ipfs/Qm...
    - http://localhost:8080/ipfs/Qm...

    :param str path: Path containing /ipfs/ and CID
    :return: Extracted CID string, or original path if no /ipfs/ found
    :rtype: str
    """
    # Only parse if it looks like a path/URL (contains /ipfs/ and is not just a CID)
    if "/ipfs/" not in path:
        return path

    patterns = [
        r"/ipfs/([^/?#]+)",  # /ipfs/CID
        r"ipfs\.io/ipfs/([^/?#]+)",  # https://ipfs.io/ipfs/CID
        r"localhost:\d+/ipfs/([^/?#]+)",  # http://localhost:8080/ipfs/CID
    ]

    for pattern in patterns:
        match = re.search(pattern, path)
        if match:
            return match.group(1)

    return path  # No /ipfs/ path found, return as-is


def from_string(cidstr: str) -> CIDv0 | CIDv1:
    """
    Creates a CID object from a encoded form

    Automatically extracts CID from /ipfs/ paths if present.

    :param str cidstr: can be

        - base58-encoded multihash
        - multihash
        - multibase-encoded multihash
        - /ipfs/ path containing CID
        - URL containing /ipfs/ path
    :return: a CID object
    :rtype: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
    """
    # Extract CID from /ipfs/ path if present (only for strings)
    if isinstance(cidstr, str):
        cidstr = parse_ipfs_path(cidstr)
    cidbytes = ensure_bytes(cidstr, "utf-8")
    return from_bytes(cidbytes)


def from_bytes(cidbytes: bytes) -> CIDv0 | CIDv1:
    """
    Creates a CID object from a encoded form

    :param bytes cidbytes: can be

        - base58-encoded multihash
        - multihash
        - multibase-encoded multihash
    :return: a CID object
    :rtype: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
    :raises: `ValueError` if the base58-encoded string is not a valid string
    :raises: `ValueError` if the length of the argument is zero
    :raises: `ValueError` if the length of decoded CID is invalid
    """
    if len(cidbytes) < 2:
        msg = "argument length can not be zero"
        raise ValueError(msg)

    # first byte for identity multibase and CIDv0 is 0x00
    # putting in assumption that multibase for CIDv0 can not be identity
    # refer: https://github.com/ipld/cid/issues/13#issuecomment-326490275
    if cidbytes[0] != 0 and multibase.is_encoded(cidbytes):
        # if the bytestream is multibase encoded
        cid = cast(bytes, multibase.decode(cidbytes))

        if len(cid) < 2:
            msg = "cid length is invalid"
            raise ValueError(msg)

        data = cid[1:]
        version = int(cid[0])
        codec = multicodec.get_codec(data)
        multihash = multicodec.remove_prefix(data)
    elif cidbytes[0] in (0, 1):
        # if the bytestream is a CID
        version = cidbytes[0]
        data = cidbytes[1:]
        codec = multicodec.get_codec(data)
        multihash = multicodec.remove_prefix(data)
    else:
        # otherwise its just base58-encoded multihash
        try:
            version = 0
            codec = CIDv0.CODEC
            multihash = base58.b58decode(cidbytes)
        except ValueError:
            msg = "multihash is not a valid base58 encoded multihash"
            raise ValueError(msg) from None

    try:
        mh.decode(multihash)
    except ValueError:
        raise

    return make_cid(version, codec, multihash)


def extract_encoding(cid_str: str) -> str:
    """
    Extract multibase encoding from CID string without fully parsing it.

    :param str cid_str: CID string
    :return: Encoding name (e.g., "base58btc", "base32")
    :rtype: str
    :raises ValueError: if the CID string is too short or invalid
    """
    if len(cid_str) < 2:
        msg = "CID string too short"
        raise ValueError(msg)

    # CIDv0 detection (Base58BTC, 46 chars, starts with "Qm")
    if len(cid_str) == 46 and cid_str.startswith("Qm"):
        return "base58btc"

    # CIDv1: first character is multibase encoding
    encoding_char = cid_str[0]
    try:
        # Get encoding from multibase using the first character
        encoding_info = multibase.get_codec(encoding_char)
        return encoding_info.encoding
    except (ValueError, KeyError, AttributeError) as e:
        msg = f"Invalid multibase encoding: {encoding_char}"
        raise ValueError(msg) from e


def from_bytes_strict(cidbytes: bytes) -> CIDv0 | CIDv1:
    """
    Parse CID from bytes, validating that there are no trailing bytes.

    This is a strict version of from_bytes() that ensures all input bytes
    are consumed during parsing.

    :param bytes cidbytes: CID bytes to parse
    :return: CID object
    :rtype: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
    :raises ValueError: if there are trailing bytes or parsing fails
    """
    cid = from_bytes(cidbytes)

    # Calculate expected length
    if cid.version == 0:
        expected_len = len(cid.multihash)  # CIDv0 is just multihash
    else:
        # CIDv1: <version><codec><multihash>
        # Version is 1 byte, codec is varint, multihash is variable
        codec_prefix = multicodec.get_prefix(cid.codec)
        expected_len = 1 + len(codec_prefix) + len(cid.multihash)

    # Check for trailing bytes
    if len(cidbytes) > expected_len:
        msg = "trailing bytes in CID data"
        raise ValueError(msg)

    return cid


def from_reader(reader) -> tuple[int, CIDv0 | CIDv1]:
    """
    Parse CID from reader/stream.

    Reads bytes incrementally from the reader and parses a CID,
    returning the number of bytes read and the CID object.

    :param reader: File-like object with read() method
    :return: Tuple of (bytes_read, CID)
    :rtype: tuple[int, :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`]
    :raises ValueError: if parsing fails
    """
    # Read first byte to determine version
    first_byte = reader.read(1)
    if not first_byte:
        msg = "Not enough data to read CID"
        raise ValueError(msg)

    version = int(first_byte[0])

    if version == 0:
        # CIDv0: just read the multihash
        # We need to determine multihash length
        # Read enough bytes to determine length (multihash has length prefix)
        peek = reader.read(2)
        if len(peek) < 2:
            msg = "Not enough data to read CIDv0 multihash"
            raise ValueError(msg)

        # Multihash format: <code><length><digest>
        # Length is second byte
        mh_length = int(peek[1])
        # Total multihash length: 2 bytes (code + length) + digest length
        remaining = mh_length
        multihash_bytes = first_byte + peek + reader.read(remaining)

        bytes_read = len(multihash_bytes)
        cid = from_bytes(multihash_bytes)
        return bytes_read, cid

    elif version == 1:
        # CIDv1: <version><codec-varint><multihash>
        # Read codec (varint)
        codec_bytes = bytearray()
        codec_bytes.append(first_byte[0])
        bytes_read = 1

        # Read varint for codec
        while True:
            byte = reader.read(1)
            if not byte:
                msg = "Not enough data to read CIDv1 codec"
                raise ValueError(msg)
            codec_bytes.append(byte[0])
            bytes_read += 1
            if (byte[0] & 0x80) == 0:
                break

        # Now read multihash
        # Peek to get multihash length
        peek = reader.read(2)
        if len(peek) < 2:
            msg = "Not enough data to read CIDv1 multihash"
            raise ValueError(msg)

        mh_length = int(peek[1])
        remaining = mh_length
        multihash_bytes = reader.read(remaining)
        if len(multihash_bytes) < remaining:
            msg = "Not enough data to read CIDv1 multihash"
            raise ValueError(msg)

        codec_bytes.extend(peek)
        codec_bytes.extend(multihash_bytes)
        bytes_read += len(peek) + len(multihash_bytes)

        cid = from_bytes(bytes(codec_bytes))
        return bytes_read, cid

    else:
        msg = f"Invalid CID version: {version}"
        raise ValueError(msg)


def must_parse(v: str | bytes) -> CIDv0 | CIDv1:
    """
    Parse CID, raising exception on error.

    This is a convenience function that always raises an exception
    on parsing failure (unlike make_cid which also raises exceptions).

    :param v: CID string or bytes
    :type v: str or bytes
    :return: CID object
    :rtype: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
    :raises ValueError: if parsing fails
    """
    try:
        return make_cid(v)
    except ValueError as e:
        msg = f"Failed to parse CID: {e}"
        raise ValueError(msg) from e


class CIDJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for CID objects.

    Encodes CID objects to IPLD JSON format: {"/": "<cid-string>"}
    """

    def default(self, obj: Any) -> Any:  # type: ignore[override]
        if isinstance(obj, (CIDv0, CIDv1)):
            return obj.to_json_dict()
        return super().default(obj)
