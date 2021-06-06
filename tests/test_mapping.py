import hypothesis.strategies as st
from hypothesis import given

from pyradixtree.mapping import RadixTreeMap


@given(st.dictionaries(st.text(min_size=1), st.integers()))
def test_insert_items(values):
    rtm = RadixTreeMap()
    for key, value in values.items():
        rtm[key] = value
    for key, value in values.items():
        assert rtm[key] == value


@given(st.dictionaries(st.text(min_size=1), st.integers()))
def test_delete_items(values):
    rtm = RadixTreeMap()
    for key, value in values.items():
        rtm[key] = value
    for key, _ in values.items():
        del rtm[key]
    assert len(rtm) == 0


@given(st.dictionaries(st.text(min_size=1), st.integers()))
def test_iterate_items(values):
    rtm = RadixTreeMap()
    for key, value in values.items():
        rtm[key] = value
    assert set(rtm.keys()) == set(values.keys())


@given(st.dictionaries(st.text(min_size=1), st.integers()))
def test_overwrite_items(values):
    rtm = RadixTreeMap()
    for key, _ in values.items():
        rtm[key] = 1
    for key, value in values.items():
        rtm[key] = value
    for key, value in values.items():
        assert rtm[key] == value
