"""Builder pattern for CID construction."""

from abc import ABC, abstractmethod
import hashlib
from typing import TYPE_CHECKING

import multihash

if TYPE_CHECKING:
    from .cid import CIDv0, CIDv1


class Builder(ABC):
    """Builder interface for CID construction."""

    @abstractmethod
    def sum(self, data: bytes) -> "CIDv0 | CIDv1":
        """
        Hash data and create CID.

        :param bytes data: Data to hash
        :return: CID object
        :rtype: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
        """
        pass

    @abstractmethod
    def get_codec(self) -> str:
        """
        Get current codec.

        :return: Codec name
        :rtype: str
        """
        pass

    @abstractmethod
    def with_codec(self, codec: str) -> "Builder":
        """
        Return new builder with different codec.

        :param str codec: New codec name
        :return: New builder instance
        :rtype: :py:class:`cid.builder.Builder`
        """
        pass


class V0Builder(Builder):
    """Builder for CIDv0."""

    def sum(self, data: bytes) -> "CIDv0":
        """
        Create CIDv0 from data.

        :param bytes data: Data to hash
        :return: CIDv0 object
        :rtype: :py:class:`cid.CIDv0`
        """
        from .cid import CIDv0

        digest = hashlib.sha256(data).digest()
        mhash = multihash.encode(digest, "sha2-256")
        return CIDv0(mhash)

    def get_codec(self) -> str:
        """
        Get current codec (always "dag-pb" for CIDv0).

        :return: Codec name
        :rtype: str
        """
        return "dag-pb"

    def with_codec(self, codec: str) -> Builder:
        """
        Return new builder with different codec.

        Changing codec from CIDv0 requires switching to V1Builder.

        :param str codec: New codec name
        :return: New builder instance (V1Builder if codec changed)
        :rtype: :py:class:`cid.builder.Builder`
        """
        if codec == "dag-pb":
            return self
        # Changing codec requires V1
        return V1Builder(codec=codec, mh_type="sha2-256")


class V1Builder(Builder):
    """Builder for CIDv1."""

    def __init__(self, codec: str, mh_type: str, mh_length: int = -1) -> None:
        """
        Create V1Builder.

        :param str codec: Codec name
        :param str mh_type: Multihash type
        :param int mh_length: Multihash length (-1 for default)
        """
        self.codec = codec
        self.mh_type = mh_type
        self.mh_length = mh_length

    def sum(self, data: bytes) -> "CIDv1":
        """
        Create CIDv1 from data.

        :param bytes data: Data to hash
        :return: CIDv1 object
        :rtype: :py:class:`cid.CIDv1`
        """
        from .cid import CIDv1

        if self.mh_type == "sha2-256":
            digest = hashlib.sha256(data).digest()
        elif self.mh_type == "sha2-512":
            digest = hashlib.sha512(data).digest()
        else:
            msg = f"Hash type {self.mh_type} not fully implemented"
            raise NotImplementedError(msg)

        mh_length = None if self.mh_length == -1 else self.mh_length
        mhash = multihash.encode(digest, self.mh_type, mh_length)
        return CIDv1(self.codec, mhash)

    def get_codec(self) -> str:
        """
        Get current codec.

        :return: Codec name
        :rtype: str
        """
        return self.codec

    def with_codec(self, codec: str) -> Builder:
        """
        Return new builder with different codec.

        :param str codec: New codec name
        :return: New builder instance
        :rtype: :py:class:`cid.builder.Builder`
        """
        if codec == self.codec:
            return self
        return V1Builder(codec=codec, mh_type=self.mh_type, mh_length=self.mh_length)
