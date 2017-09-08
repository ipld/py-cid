# -*- coding: utf-8 -*-
import base58

import multibase

from morphys import ensure_bytes, ensure_unicode

import multicodec


class BaseCID(object):
    __hash__ = object.__hash__

    def __init__(self, version, codec, multihash):
        self._version = version
        self._codec = codec
        self._multihash = ensure_bytes(multihash)

    @property
    def version(self):
        return self._version

    @property
    def codec(self):
        return self._codec

    @property
    def multihash(self):
        return self._multihash

    @property
    def buffer(self):
        raise NotImplementedError

    def encode(self, *args, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        def truncate(s, length):
            return s[:length] + b'..' if len(s) > length else s

        truncate_length = 20
        return '{class_}(version={version}, codec={codec}, multihash={multihash})'.format(
            class_=self.__class__.__name__,
            version=self._version,
            codec=self._codec,
            multihash=truncate(self._multihash, truncate_length),
        )

    def __str__(self):
        return ensure_unicode(self.encode())

    def __eq__(self, other):
        return (self.version == other.version) and (self.codec == other.codec) and (self.multihash == other.multihash)


class CIDv0(BaseCID):
    CODEC = 'dag-pb'

    def __init__(self, multihash):
        super(CIDv0, self).__init__(0, self.CODEC, multihash)

    @property
    def buffer(self):
        return self.multihash

    def encode(self):
        return base58.b58encode(self.buffer)

    def to_v1(self):
        return CIDv1(self.CODEC, self.multihash)


class CIDv1(BaseCID):
    def __init__(self, codec, multihash):
        super(CIDv1, self).__init__(1, codec, multihash)

    @property
    def buffer(self):
        return b''.join([bytes([self.version]), multicodec.add_prefix(self.codec, self.multihash)])

    def encode(self, encoding='base58btc'):
        return multibase.encode(encoding, self.buffer)

    def to_v0(self):
        if self.codec != CIDv0.CODEC:
            raise ValueError('CIDv1 can only be converted for codec {}'.format(CIDv0.CODEC))

        return CIDv0(self.multihash)


def make_cid(*args):
    """

    :param args: can be multiple types
        make_cid(<base58 encoded multihash CID>) -> CIDv0
        make_cid(<multihash CID>) -> CIDv0
        make_cid(<multibase encoded multihash CID>) -> CIDv1
        make_cid(<version>, <codec>, <multihash>) -> CIDv1
    :return: CIDv0 or CIDv1
    """
    if len(args) == 1:
        data = args[0]
        if isinstance(data, str):
            return from_string(data)
        elif isinstance(data, bytes):
            return from_bytes(data)
        else:
            raise ValueError('invalid argument passed, expected: str or byte, found: {}'.format(type(data)))

    elif len(args) == 3:
        version, codec, multihash = args
        if version not in (0, 1):
            raise ValueError('version should be 0 or 1, {} was provided'.format(version))
        if not multicodec.is_codec(codec):
            raise ValueError('invalid codec {} provided, please check'.format(codec))
        if not (isinstance(multihash, str) or isinstance(multihash, bytes)):
            raise ValueError('invalid type for multihash provided, should be str or bytes')

        if version == 0:
            if codec != CIDv0.CODEC:
                raise ValueError('codec for version 0 can only be {}, found: {}'.format(CIDv0.CODEC, codec))
            return CIDv0(multihash)
        else:
            return CIDv1(codec, multihash)
    else:
        raise ValueError('invalid number of arguments, expected 1 or 3')


def is_cid(cidstr):
    try:
        return bool(make_cid(cidstr))
    except ValueError:
        return False


def from_string(cidstr):
    cidbytes = ensure_bytes(cidstr, 'utf-8')
    return from_bytes(cidbytes)


def from_bytes(cidbytes):
    if multibase.is_encoded(cidbytes):
        # if the bytestream is multibase encoded
        cid = multibase.decode(cidbytes)
        data = cid[1:]
        version = int(cid[0])
        codec = multicodec.get_codec(data)
        multihash = multicodec.remove_prefix(data)

        return make_cid(version, codec, multihash)
    elif cidbytes[0] in (0, 1):
        # if the bytestream is a CID
        version = cidbytes[0]
        data = cidbytes[1:]
        codec = multicodec.get_codec(data)
        multihash = multicodec.remove_prefix(data)

        return make_cid(version, codec, multihash)
    else:
        # otherwise its just base58-encoded multihash
        return make_cid(0, CIDv0.CODEC, base58.b58decode(cidbytes))
