from dataclasses import replace
from itertools import zip_longest
from typing import List, Tuple, TypeVar

from pyradixtree.node import Node, Sentinel
from pyradixtree.operations._find import _compare_find

T = TypeVar("T")


def _compare_insert(search: str, prefix: str) -> Tuple[str, str, str]:
    """
    Helper function for insert used to find common prefix and dangling
    end.
    """
    common: List[str] = []
    acc_left: List[str] = []
    acc_right: List[str] = []
    for (s, p) in zip_longest(search, prefix):
        if s is None:
            # search is shorter than prefix
            acc_left.append(p)
        elif p is None:
            # search is longer than prefix, but contains prefix
            acc_right.append(s)
        elif s == p:
            common.append(s)
        else:
            break
    return "".join(common), "".join(acc_left), "".join(acc_right)


def _insert_root(key: str, value: T, path: List[Node[T]]) -> None:
    """
    For example if tree already contains 'slow' and we need to add
    'slower'.

    :param key: key to insert, relative to the insertion root
    :param value: value to insert
    :param path: path to the insertion
    """
    current_root = path[-1]
    new_node = Node(
        key=key,
        value=value,
        children=[],
    )
    current_root.children.append(new_node)


def _insert_root_split(key: str, common: str, value: T, path: List[Node[T]]) -> None:
    """
    For example if the tree already contains 'tester' to add 'test', we
    take their common prefix 'test' and add in 'test' -> 'er'. Also if the tree already
    contains 'test', to insert 'team', we take their common prefix 'te' and then split ]
    'te' -> 'st' and 'te' -> 'am'. Also if the tree already contains 'test' and 'team',
    to insert 'toast' we split at their common prefix 't', into 't' -> 'e' and
    't' -> 'oast', then connect 't' -> 'e' -> 'st' and 't' -> 'e' -> 'am'.

    :param key: key to insert, relative to the insertion root
    :param common: common value between key and end of path
    :param value: value to insert
    :param path: path to the insertion
    """
    current_end: Node[T] = path[-1]
    # compute the new keys
    if current_end.key is not None:
        left_key = current_end.key[len(common) :]
        right_key = key[len(common) :]
        # create new nodes at the split
        left_node = replace(current_end, key=left_key)
        right_node = Node(
            key=right_key,
            value=value,
            children=[],
        )
        # create new common root
        current_end.key = common
        current_end.value = Sentinel.MISSING
        current_end.children = [
            left_node,
            right_node,
        ]
    else:
        raise ValueError("Passed incompatible path")


def insert(key: str, value: T, tree: Node[T], update: bool = True) -> None:
    """
    Insert the given key and value pair into the tree, if the value already exist then
    update it if update is set to True.

    :param key: given key to insert or modify
    :param value: given value
    :param tree: given radix tree
    :param update: whether to update the value if found
    """
    path: List[Node[T]] = []
    acc: List[Tuple[Node[T], str]] = [(tree, key)]
    while acc:
        item, search = acc.pop()
        if item.is_root:
            path.append(item)
            acc.extend((node, search) for node in item.children)
        else:
            comparison = _compare_find(search, item.key)
            if comparison is None and item.key is not None:
                common, left, right = _compare_insert(search, item.key)
                if common:
                    path.append(item)
                    _insert_root_split(search, common, value, path)
                    break
                else:
                    continue
            elif comparison == "" and item.value != Sentinel.MISSING:
                # found the item, modify it
                if update:
                    item.value = value
                break
            elif comparison is not None:
                # found a prefix, focus search
                path.append(item)
                acc = [(node, comparison) for node in item.children]
            else:
                # above is to satisfy mypy
                continue
    else:
        if path[-1].key is None:
            # special case of inserting at the root
            right = key
        else:
            _, _, right = _compare_insert(key, path[-1].key)
        _insert_root(right, value, path)
