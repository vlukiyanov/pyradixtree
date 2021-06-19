import pytest
from hypothesis.strategies import SearchStrategy

from pyradixtree.node import Node, Sentinel
from pyradixtree.operations._find import _compare_find, find


def test_compare_find_simple_exist():
    assert _compare_find("abba", "ab") == "ba"
    assert _compare_find("abcef", "abce") == "f"
    assert _compare_find("abcef", "") == "abcef"
    assert _compare_find("aa", "a") == "a"


def test_compare_find_simple_not_exist():
    assert _compare_find("abba", "ba") is None
    assert _compare_find("abcef", "f") is None
    assert _compare_find("aa", "b") is None


def test_compare_find_simple_match():
    assert _compare_find("abc", "abc") == ""
    assert _compare_find("aa", "aa") == ""
    assert _compare_find("", "") == ""


def test_find_simple_example_1():
    tree = Node(
        key=None,
        children=[
            Node(
                key="test",
                children=[
                    Node(key="er", children=[], value=1),
                    Node(key="", children=[], value=2),
                ],
                value=Sentinel.MISSING,
            )
        ],
        value=Sentinel.MISSING,
    )
    assert find("tester", tree)[0] == 1
    assert find("test", tree)[0] == 2


def test_find_simple_example_2():
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[
            Node(
                key="ab",
                value=Sentinel.MISSING,
                children=[
                    Node(key="ba", value="squirrel", children=[]),
                    Node(
                        key="c",
                        value=Sentinel.MISSING,
                        children=[
                            Node(key="", value="three", children=[]),
                            Node(key="d", value="four", children=[]),
                        ],
                    ),
                ],
            )
        ],
    )
    # values
    assert find("abba", tree)[0] == "squirrel"
    with pytest.raises(KeyError):
        _ = find("abb", tree)[0]
    with pytest.raises(KeyError):
        _ = find("bba", tree)[0] is None
    assert find("abc", tree)[0] == "three"
    assert find("abcd", tree)[0] == "four"
    with pytest.raises(KeyError):
        assert find("ab", tree)[0] is None
    # paths
    assert len(find("abba", tree)[1]) == 3
    assert len(find("abc", tree)[1]) == 4
    assert len(find("abcd", tree)[1]) == 4
    # handling of return_path
    assert len(find("abba", tree, return_path=False)[1]) == 0
    assert len(find("abc", tree, return_path=False)[1]) == 0
    assert len(find("abcd", tree, return_path=False)[1]) == 0
