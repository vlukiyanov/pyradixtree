import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from pyradixtree.node import Node, Sentinel, pretty_path
from pyradixtree.operations import find, length
from pyradixtree.operations._insert import (
    ComparisonResult,
    _compare_insert,
    _insert_root,
    _insert_root_split,
    insert,
)


def test_compare_insert():
    assert _compare_insert("abba", "ab") == ComparisonResult(
        common="ab", right_dangling="", left_dangling="ba"
    )
    assert _compare_insert("ab", "abba") == ComparisonResult(
        common="ab", right_dangling="ba", left_dangling=""
    )


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
        _ = find("water", tree) is None
    _insert_root("water", 3, path)
    assert len(tree.children) == 3
    assert find("water", tree) == 3


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
        _ = find("slower", tree)
    _insert_root("er", 4, path)
    assert len(tree.children[1].children) == 2
    assert tree.children[1].children[0].key == "er"
    assert find("slower", tree) == 4
    assert find("slow", tree) == 2


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
        _ = find("test", tree)
    assert find("tester", tree) == 1
    _insert_root_split("test", "test", 2, path)
    assert len(tree.children) == 1
    assert find("test", tree) == 2
    assert find("tester", tree) == 1


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
        _ = find("team", tree)
    assert find("test", tree) == 1
    _insert_root_split("team", "te", 2, path)
    assert len(tree.children) == 1
    assert find("team", tree) == 2
    assert find("test", tree) == 1


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
    assert find("test", tree) == 1
    assert find("team", tree) == 2
    with pytest.raises(KeyError):
        _ = find("toast", tree)
    _insert_root_split("toast", "t", 3, path)
    assert len(tree.children) == 1
    assert find("test", tree) == 1
    assert find("team", tree) == 2
    assert find("toast", tree) == 3


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
        _ = find("slower", tree)
    insert("slower", 4, tree)
    assert find("slower", tree) == 4


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
        _ = find("team", tree)
    insert("team", 2, tree)
    assert find("team", tree) == 2


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
        _ = find("team", tree)
    insert("team", 2, tree)
    assert find("team", tree) == 2


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
        _ = find("toast", tree)
    insert("toast", 3, tree)
    assert find("toast", tree) == 3
    # test update functionality
    insert("toast", 4, tree, update=False)
    assert find("toast", tree) == 3
    insert("toast", 4, tree, update=True)
    assert find("toast", tree) == 4
    insert("toast", 5, tree, update=True)
    assert find("toast", tree) == 5


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
        _ = find("roast", tree)
    insert("roast", 3, tree)
    assert find("roast", tree) == 3


def test_insert_hand_written_example_6():
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[],
    )
    items = ["1", "102", "114"]
    inserted = []
    for index, item in enumerate(items):
        insert(item, index, tree)
        inserted.append([index, item])
        for inserted_index, inserted_item in inserted:
            assert inserted_index == find(inserted_item, tree)
    for index, item in enumerate(items):
        assert index == find(item, tree)


def test_insert_hand_written_example_7():
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[],
    )
    items = ["-110000000", "-100", "-4", "-12"]
    inserted = []
    for index, item in enumerate(items):
        insert(item, index, tree)
        inserted.append([index, item])
        for inserted_index, inserted_item in inserted:
            assert inserted_index == find(inserted_item, tree)
    for index, item in enumerate(items):
        assert index == find(item, tree)


@given(st.sets(st.text(min_size=1, max_size=20480), min_size=1, max_size=20480))
@settings(deadline=None)
def test_insert_random_example_text(items):
    # insert random texts, check that they exist in the tree
    # totally random texts are unlikely to hit issues with branching
    items = list(items)
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[],
    )
    for item in items:
        with pytest.raises(KeyError):
            _ = find(item, tree)
    for index, item in enumerate(items):
        insert(item, index, tree)
    for index, item in enumerate(items):
        recovered_index = find(item, tree)
        assert index == recovered_index
    assert length(tree) == len(items)


@given(st.sets(st.integers(), min_size=1, max_size=20480))
@settings(deadline=None)
def test_insert_random_example_integers(items):
    # insert random strings of integers, check that they exist in the tree
    # totally random texts are unlikely to hit issues with branching
    items = [str(item) for item in items]
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[],
    )
    for item in items:
        with pytest.raises(KeyError):
            _ = find(item, tree)
    for index, item in enumerate(items):
        insert(item, index, tree)
    for index, item in enumerate(items):
        recovered_index = find(item, tree)
        assert index == recovered_index
    assert length(tree) == len(items)


@given(st.integers(min_value=1, max_value=1024))
@settings(deadline=None)
def test_insert_random_example_integers_dense(number):
    items = [str(item) for item in range(number)]
    tree = Node(
        key=None,
        value=Sentinel.MISSING,
        children=[],
    )
    for item in items:
        with pytest.raises(KeyError):
            _ = find(item, tree)
    for index, item in enumerate(items):
        insert(item, index, tree)
    for index, item in enumerate(items):
        recovered_index = find(item, tree)
        assert index == recovered_index
    assert length(tree) == len(items)
