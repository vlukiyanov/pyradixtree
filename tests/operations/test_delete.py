from pyradixtree.node import Node, Sentinel
from pyradixtree.operations import delete, find, insert, length


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
    assert find("b", tree)[0] == 1
    assert find("abc", tree)[0] == 2
    assert delete("b", tree) == "b"
    assert length(tree) == 1
    assert find("abc", tree)[0] == 2
    assert delete("abc", tree) == "abc"
    assert length(tree) == 0
    assert delete("a", tree) is None
    assert delete("b", tree) is None
    assert delete("abc", tree) is None
