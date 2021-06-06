import pytest

from pyradixtree.node import Node, Sentinel
from pyradixtree.operations import find, insert, length, modify


def test_modify_hand_written_example():
    """
    If the tree contains 'a', 'b', and 'abc', modify their values and check modifications
    persist.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[],
    )
    insert("a", 0, tree)
    insert("b", 1, tree)
    insert("abc", 2, tree)
    assert length(tree) == 3
    # modify a, which exists
    assert modify("a", -1, tree) == "a"
    assert length(tree) == 3
    assert find("a", tree)[0] == -1
    # modify c, which does not exist
    assert modify("c", -1, tree) is None
    assert length(tree) == 3
    with pytest.raises(KeyError):
        assert find("c", tree)
