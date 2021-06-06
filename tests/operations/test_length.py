import pytest

from pyradixtree.node import Node, Sentinel
from pyradixtree.operations import find, insert, delete
from pyradixtree.operations._length import length


def test_length_hand_written_example_1():
    """
    If the tree contains 'a', 'b', and 'c', then length is 3, if we add
    'ab', 'ca', and 'cd' then the length is 6.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[
            Node(
                key="a",
                value=1,
                children=[],
            ),
            Node(
                key="b",
                value=2,
                children=[],
            ),
            Node(
                key="c",
                value=3,
                children=[],
            ),
        ],
    )
    assert length(tree) == 3
    insert("ab", 0, tree)
    insert("ba", 0, tree)
    insert("cd", 0, tree)
    assert length(tree) == 6


def test_length_hand_written_example_2():
    """
    If the tree contains 'a', 'b', and 'c', then length is 3, if they are removed it
    has length 0.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[],
    )
    assert length(tree) == 0
    insert("ab", 0, tree)
    insert("ba", 0, tree)
    insert("cd", 0, tree)
    assert length(tree) == 3
    delete("ab", tree)
    delete("ba", tree)
    delete("cd", tree)
    assert length(tree) == 0
