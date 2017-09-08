import multihash
import pytest

import multibase
import multicodec
from cid import CIDv0, CIDv1, make_cid, is_cid
from multibase.multibase import CODECS


@pytest.fixture(scope='session')
def test_hash():
    return multihash.digest(b'hello world', 'sha2-256').encode()


class CIDv0TestCase(object):
    @pytest.fixture()
    def cid(self, test_hash):
        return CIDv0(test_hash)

    def test_init(self, cid, test_hash):
        """ #__init__: initializes all the attributes correctly """
        assert cid.version == 0
        assert cid.codec == CIDv0.CODEC
        assert cid.multihash == test_hash

    def test_buffer(self, cid, test_hash):
        """ .buffer: is computed properly """
        assert cid.buffer == test_hash

    def test_encode(self, cid):
        """ #encode: base58 encodes the buffer by default """
        assert cid.encode() == 'QmaozNR7DZHQK1ZcU9p7QdrshMvXqWK6gpu5rmrkPdT3L4'


class CIDv1TestCase(object):
    TEST_CODEC = 'dag-pb'

    @pytest.fixture()
    def cid(self, test_hash):
        return CIDv1(self.TEST_CODEC, test_hash)

    def test_init(self, cid, test_hash):
        """ #__init__: attributes are set properly """
        assert cid.version == 1
        assert cid.codec == self.TEST_CODEC
        assert cid.multihash == test_hash

    def test_buffer(self, cid):
        """ .buffer: buffer is computed properly """
        buffer = cid.buffer
        assert buffer[0] == 1
        assert buffer[1:] == multicodec.add_prefix(self.TEST_CODEC, cid.multihash)

    def test_encode_default(self, cid):
        """ #encode defaults to base58btc encoding """
        assert cid.encode() == b'zdj7WhuEjrB52m1BisYCtmjH1hSKa7yZ3jEZ9JcXaFRD51wVz'

    @pytest.mark.parametrize('codec', CODECS)
    def test_encode_encoding(self, cid, codec):
        """ #encode uses the encoding provided for encoding """
        assert cid.encode(codec.encoding) == multibase.encode(codec.encoding, cid.buffer)


class CIDTestCase(object):
    def test_cidv0_eq_cidv0(self, test_hash):
        """ check for equality for CIDv0 for same hash """
        assert CIDv0(test_hash) == make_cid(CIDv0(test_hash).encode())

    def test_cidv0_neq(self):
        """ check for inequality for CIDv0 for different hashes """
        assert CIDv0(b'QmdfTbBqBPQ7VNxZEYEj14VmRuZBkqFbiwReogJgS1zR1n') != \
            CIDv0(b'QmdfTbBqBPQ7VNxZEYEj14VmRuZBkqFbiwReogJgS1zR1o')

    def test_cidv0_eq_cidv1(self, test_hash):
        """ check for equality between converted v0 to v1 """
        assert CIDv0(test_hash).to_v1() == CIDv1(CIDv0.CODEC, test_hash)

    def test_cidv1_eq_cidv0(self):
        """ check for equality between converted v1 to v0 """
        assert CIDv1(CIDv0.CODEC, test_hash).to_v0() == CIDv0(test_hash)

    def test_cidv1_to_cidv0_no_dag_pb(self):
        """ converting non dag-pb CIDv1 should raise an exception """
        with pytest.raises(ValueError) as excinfo:
            CIDv1('base2', test_hash).to_v0()
        assert 'can only be converted for codec' in str(excinfo.value)

    def test_is_cid_valid(self, test_hash):
        assert is_cid(CIDv0(test_hash).encode())

    @pytest.mark.parametrize('test_data', (
        'foobar',
        b'foobar',
        multibase.encode('base58btc', b'foobar'),
    ))
    def test_is_cid_invalid(self, test_data):
        assert not is_cid(test_data)


class MakeCIDTestCase(object):
    def test_hash(self):
        pass

    def test_hash_invalid_type(self):
        pass

    def test_version_invalid(self):
        pass

    def test_codec_invalid(self):
        pass

    def test_multihash_invalid(self):
        pass

    def test_version_0_invalid_codec(self):
        pass


class FromStringTestCase(object):
    def test_multibase_encoded_hash(self):
        pass

    def test_base58_encoded_hash(self):
        pass

    def test_cid(self):
        pass


class FromBytesTestCase(FromStringTestCase):
    pass
