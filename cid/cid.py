# -*- coding: utf-8 -*-
import base58

import multibase

from morphys import ensure_bytes

import multicodec


class CID(object):
    __hash__ = object.__hash__

    def __init__(self, version, codec, multihash):
        self._version = version
        self._codec = codec
        self._multihash = multihash

    @property
    def version(self):
        return self._version

    @property
    def codec(self):
        return self._codec

    @property
    def multihash(self):
        return self._multihash

    @classmethod
    def is_cid(self, cidstr):
        pass

    @classmethod
    def from_string(cls, cidstr):
        cidbytes = ensure_bytes(cidstr, 'utf-8')
        return cls.from_bytes(cidbytes)

    @classmethod
    def from_bytes(cls, cidbytes):
        if multibase.is_encoded(cidbytes):
            cid = multibase.decode(cidbytes)
            data = cid[1:]
            version = int(cid[0])
            codec = multicodec.get_codec(data)
            multihash = multicodec.remove_prefix(data)

            return cls(version, codec, multihash)
        else:
            raise ValueError('input is not multibase encoded')

    @classmethod
    def from_multihash(cls, multihash):
        return cls(0, 'dag-pb', multihash)

    @classmethod
    def from_b58_multihash(cls, b58_multihash):
        multihash = base58.b58decode(b58_multihash)
        return cls.from_multihash(multihash)

    @classmethod
    def from_cid(cls, cid):
        if multibase.is_encoded(cid):
            cid = multibase.decode(cid)

    def _buffer(self):
        if self.version == 0:
            return self.multihash
        elif self.version == 1:
            return b''.join([self.version, multicodec.add_prefix(self.codec, self.multihash)])

    def to_base_encoded_string(self, base='base58btc'):
        return multibase.encode(base, self._buffer())

    def __str__(self):
        if self._version == 0:
            return '{}{}{}'.format(self._version, self._codec, self._multihash.decode('utf-8'))
        elif self._version == 1:
            return

    def __repr__(self):
        truncate = lambda x, l: (x[:l] + '..' if len(x) > l else x)

        return '{class_}(version={version}, codec={codec}, multihash={multihash})'.format(
            class_=self.__class__.__name__,
            version=self._version,
            codec=self._codec,
            multihash=truncate(self._multihash, 50),
        )

    def __eq__(self, other):
        return (self.version == other.version) and (self.codec == other.codec) and (self.multihash == other.multihash)
