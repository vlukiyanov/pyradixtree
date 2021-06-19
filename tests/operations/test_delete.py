from pyradixtree.node import Node, Sentinel
from pyradixtree.operations import delete, find, insert, length


def test_delete_simple_example():
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[],
    )
    insert("10", 0, tree)
    insert("1", 0, tree)
    assert length(tree) == 2
    assert delete("10", tree) == "10"
    assert length(tree) == 1
    assert delete("1", tree) == "1"
    assert length(tree) == 0


def test_delete_hand_written_example():
    """
    If the tree contains 'a', 'b', and 'abc', delete 'a', then 'b' and make sure
    'abc' remains.
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
    assert delete("a", tree) == "a"
    assert length(tree) == 2
    assert find("b", tree) == 1
    assert find("abc", tree) == 2
    assert delete("b", tree) == "b"
    assert length(tree) == 1
    assert find("abc", tree) == 2
    assert delete("abc", tree) == "abc"
    assert length(tree) == 0
    assert delete("a", tree) is None
    assert delete("b", tree) is None
    assert delete("abc", tree) is None
