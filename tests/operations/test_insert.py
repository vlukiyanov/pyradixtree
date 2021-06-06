import pytest

from pyradixtree.node import Node, Sentinel
from pyradixtree.operations import find
from pyradixtree.operations._insert import (_compare_insert, _insert_root,
                                            _insert_root_split, insert)


def test_compare_insert():
    assert _compare_insert("abba", "ab") == ("ab", "", "ba")
    assert _compare_insert("ab", "abba") == ("ab", "ba", "")


def test_insert_root_hand_written_example_1():
    """
    If the tree contains 'test' and 'slow', then add 'water'.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[
            Node(
                key="test",
                value=1,
                children=[],
            ),
            Node(
                key="slow",
                value=2,
                children=[],
            ),
        ],
    )
    path = [tree]  # root
    assert len(tree.children) == 2
    with pytest.raises(KeyError):
        _ = find("water", tree)[0] is None
    _insert_root("water", 3, path)
    assert len(tree.children) == 3
    assert find("water", tree)[0] == 3


def test_insert_root_hand_written_example_2():
    """
    If the tree contains 'test', 'slow' and 'water', then add 'slower'.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[
            Node(
                key="test",
                value=1,
                children=[],
            ),
            Node(
                key="slow",
                value=2,
                children=[],
            ),
            Node(
                key="water",
                value=3,
                children=[],
            ),
        ],
    )
    path = [tree, tree.children[1]]  # root -> 'slow'
    assert not tree.children[1].children
    with pytest.raises(KeyError):
        _ = find("slower", tree)[0]
    _insert_root("er", 4, path)
    assert len(tree.children[1].children) == 1
    assert tree.children[1].children[0].key == "er"
    assert find("slower", tree)[0] == 4


def test_insert_root_split_hand_written_example_1():
    """
    If the tree contains 'tester' then add 'test'.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[
            Node(
                key="tester",
                value=1,
                children=[],
            ),
        ],
    )
    path = [tree, tree.children[0]]  # root -> 'tester'
    assert len(tree.children) == 1
    with pytest.raises(KeyError):
        _ = find("test", tree)[0]
    assert find("tester", tree)[0] == 1
    _insert_root_split("test", "test", 2, path)
    assert len(tree.children) == 1
    assert find("test", tree)[0] == 2
    assert find("tester", tree)[0] == 1


def test_insert_root_split_hand_written_example_2():
    """
    If the tree contains 'test', then add 'team'.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[
            Node(
                key="test",
                value=1,
                children=[],
            ),
        ],
    )
    path = [tree, tree.children[0]]  # root -> 'test'
    assert len(tree.children) == 1
    with pytest.raises(KeyError):
        _ = find("team", tree)[0]
    assert find("test", tree)[0] == 1
    _insert_root_split("team", "te", 2, path)
    assert len(tree.children) == 1
    assert find("team", tree)[0] == 2
    assert find("test", tree)[0] == 1


def test_insert_root_split_hand_written_example_3():
    """
    If the tree contains 'test' and 'team', then add 'toast'.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[
            Node(
                key="te",
                value=Sentinel.MISSING,
                children=[
                    Node(
                        key="st",
                        value=1,
                        children=[],
                    ),
                    Node(
                        key="am",
                        value=2,
                        children=[],
                    ),
                ],
            ),
        ],
    )
    path = [tree, tree.children[0]]  # root -> 'te'
    assert len(tree.children) == 1
    assert find("test", tree)[0] == 1
    assert find("team", tree)[0] == 2
    with pytest.raises(KeyError):
        _ = find("toast", tree)[0]
    _insert_root_split("toast", "t", 3, path)
    assert len(tree.children) == 1
    assert find("test", tree)[0] == 1
    assert find("team", tree)[0] == 2
    assert find("toast", tree)[0] == 3


def test_insert_hand_written_example_1():
    """
    If the tree contains 'test', 'slow', 'water', then add 'slower'.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[
            Node(
                key="test",
                value=1,
                children=[],
            ),
            Node(
                key="slow",
                value=2,
                children=[],
            ),
            Node(
                key="water",
                value=3,
                children=[],
            ),
        ],
    )
    with pytest.raises(KeyError):
        _ = find("slower", tree)[0]
    insert("slower", 4, tree)
    assert find("slower", tree)[0] == 4


def test_insert_hand_written_example_2():
    """
    If the tree contains 'tester' then add 'team'.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[
            Node(
                key="tester",
                value=1,
                children=[],
            ),
        ],
    )
    with pytest.raises(KeyError):
        _ = find("team", tree)[0]
    insert("team", 2, tree)
    assert find("team", tree)[0] == 2


def test_insert_hand_written_example_3():
    """
    If the tree contains 'test', then add 'team'.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[
            Node(
                key="test",
                value=1,
                children=[],
            ),
        ],
    )
    with pytest.raises(KeyError):
        _ = find("team", tree)[0]
    insert("team", 2, tree)
    assert find("team", tree)[0] == 2


def test_insert_hand_written_example_4():
    """
    If the tree contains 'test' and 'team', then add 'toast'. Also tests
    update functionality.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[
            Node(
                key="te",
                value=Sentinel.MISSING,
                children=[
                    Node(
                        key="st",
                        value=1,
                        children=[],
                    ),
                    Node(
                        key="am",
                        value=2,
                        children=[],
                    ),
                ],
            ),
        ],
    )
    with pytest.raises(KeyError):
        _ = find("toast", tree)[0]
    insert("toast", 3, tree)
    assert find("toast", tree)[0] == 3
    # test update functionality
    insert("toast", 4, tree, update=False)
    assert find("toast", tree)[0] == 3
    insert("toast", 4, tree, update=True)
    assert find("toast", tree)[0] == 4
    insert("toast", 5, tree, update=True)
    assert find("toast", tree)[0] == 5


def test_insert_hand_written_example_5():
    """
    If the tree contains nothing, add 'roast'.
    """
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[],
    )
    with pytest.raises(KeyError):
        _ = find("roast", tree)[0]
    insert("roast", 3, tree)
    assert find("roast", tree)[0] == 3
