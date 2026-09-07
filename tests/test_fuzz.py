from hypothesis import (
    given,
    settings,
    strategies as st,
)

from cid import make_cid


@given(st.binary(max_size=200))
@settings(max_examples=1000)
def test_from_bytes_never_crashes(data):
    """from_bytes should raise ValueError, KeyError, or TypeError, not crash."""
    try:
        make_cid(data)
    except (ValueError, KeyError, TypeError):
        pass  # Any exception is fine, just no crashes


@given(st.binary(min_size=34, max_size=100))
@settings(max_examples=500)
def test_cid_roundtrip_never_crashes(data):
    """CID encode/decode should never crash."""
    try:
        cid = make_cid(data)
        _ = cid.encode()
        _ = str(cid)
        _ = cid.prefix()
    except (ValueError, KeyError, TypeError):
        pass
