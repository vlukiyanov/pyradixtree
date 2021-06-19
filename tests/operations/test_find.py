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
    assert find("tester", tree) == 1
    assert find("test", tree) == 2


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
    assert find("abba", tree) == "squirrel"
    with pytest.raises(KeyError):
        _ = find("abb", tree)
    with pytest.raises(KeyError):
        _ = find("bba", tree) is None
    assert find("abc", tree) == "three"
    assert find("abcd", tree) == "four"
    with pytest.raises(KeyError):
        assert find("ab", tree) is None


def test_find_example_3():
    """
    This tests searching in a more complex example with a key that has been moved down
    after numerous splittings.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[
            Node(
                key="1",
                children=[
                    Node(key="02", children=[], value=4),
                    Node(
                        key="",
                        children=[
                            Node(key="14", children=[], value=5),
                            Node(key="", children=[], value=0),
                        ],
                        value=Sentinel.MISSING,
                    ),
                ],
                value=Sentinel.MISSING,
            )
        ],
    )
    assert find("102", tree) == 4
    assert find("114", tree) == 5
    assert find("1", tree) == 0
