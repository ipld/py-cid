"""CID Set operations for managing collections of unique CIDs."""

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cid import CIDv0, CIDv1


class CIDSet:
    """Set of unique CIDs."""

    def __init__(self) -> None:
        """Initialize an empty CID set."""
        self._set: set["CIDv0 | CIDv1"] = set()

    def add(self, cid: "CIDv0 | CIDv1") -> None:
        """
        Add CID to set.

        :param cid: CID to add
        :type cid: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
        """
        self._set.add(cid)

    def has(self, cid: "CIDv0 | CIDv1") -> bool:
        """
        Check if CID is in set.

        :param cid: CID to check
        :type cid: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
        :return: True if CID is in set, False otherwise
        :rtype: bool
        """
        return cid in self._set

    def remove(self, cid: "CIDv0 | CIDv1") -> None:
        """
        Remove CID from set.

        Does not raise an error if CID is not in set.

        :param cid: CID to remove
        :type cid: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
        """
        self._set.discard(cid)

    def __len__(self) -> int:
        """
        Get set size.

        :return: Number of CIDs in set
        :rtype: int
        """
        return len(self._set)

    def keys(self) -> list["CIDv0 | CIDv1"]:
        """
        Get all CIDs in set.

        :return: List of all CIDs in set
        :rtype: list
        """
        return list(self._set)

    def visit(self, cid: "CIDv0 | CIDv1") -> bool:
        """
        Add CID if not present, return True if added.

        :param cid: CID to visit
        :type cid: :py:class:`cid.CIDv0` or :py:class:`cid.CIDv1`
        :return: True if CID was added (was not present), False if already present
        :rtype: bool
        """
        if cid not in self._set:
            self._set.add(cid)
            return True
        return False

    def for_each(self, func: Callable[["CIDv0 | CIDv1"], None]) -> None:
        """
        Call function for each CID in set.

        :param func: Function to call for each CID
        :type func: callable
        """
        for cid in self._set:
            func(cid)

    def __iter__(self):
        """Make set iterable."""
        return iter(self._set)

    def __contains__(self, cid: "CIDv0 | CIDv1") -> bool:
        """Support 'in' operator."""
        return cid in self._set

    def __repr__(self) -> str:
        """String representation of set."""
        return f"CIDSet({len(self._set)} items)"
