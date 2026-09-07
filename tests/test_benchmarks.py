import hashlib

import pytest
import multihash

from cid import CIDv1, Prefix, make_cid


@pytest.fixture
def bench_cid():
    data = b"benchmark data" * 100
    digest = hashlib.sha256(data).digest()
    mh_bytes = multihash.encode(digest, "sha2-256")
    return CIDv1("raw", mh_bytes)


@pytest.mark.benchmark
def test_bench_cid_buffer(benchmark, bench_cid):
    benchmark(lambda: bench_cid.buffer)


@pytest.mark.benchmark
def test_bench_cid_encode(benchmark, bench_cid):
    benchmark(bench_cid.encode)


@pytest.mark.benchmark
def test_bench_cid_prefix(benchmark, bench_cid):
    benchmark(bench_cid.prefix)


@pytest.mark.benchmark
def test_bench_prefix_sum(benchmark):
    prefix = Prefix.v1(codec="raw", mh_type="sha2-256")
    data = b"benchmark data" * 100
    benchmark(prefix.sum, data)


@pytest.mark.benchmark
def test_bench_make_cid(benchmark, bench_cid):
    cid_str = str(bench_cid)
    benchmark(make_cid, cid_str)
