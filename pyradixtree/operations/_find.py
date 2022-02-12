from typing import List, Optional, Tuple, TypeVar

from pyradixtree.node import Node

T = TypeVar("T")


def _compare_find(search: str, prefix: Optional[str]) -> Optional[str]:
    """
    Helper function for find, checks whether the prefix should be explored
    for further search.

    :param search: string to search
    :param prefix: prefix to look for, either a string or None, if None
        the function returns None
    :return: None if prefix is None, otherwise the shared part of the prefix
    """
    if prefix is None:
        return None
    if search.startswith(prefix):
        return search[len(prefix) :]
    else:
        return None


def find_node(key: str, tree: Node[T]) -> Node[T]:
    """
    Find and return the value of a node in a radix tree, raise KeyError if not found.

    :param key: given key to search for
    :param tree: given radix tree to search
    :return: value
    """
    acc: List[Tuple[Node[T], str]] = [(tree, key)]
    while acc:
        item, search = acc.pop()
        if item.is_root:
            acc.extend((node, search) for node in item.children)
        else:
            comparison = _compare_find(search, item.key)
            if comparison is None:
                # item not found, continue looking through acc
                continue
            elif comparison == "" and item.is_leaf:
                # found the exact item, return it
                return item
            else:
                acc.extend((node, comparison) for node in item.children)
    # if we exhaust search without finding a prefix or the exact item, we end up here
    raise KeyError()


def find(key: str, tree: Node[T]) -> T:
    """
    Find and return the value of a node in a radix tree, raise KeyError if not found.

    :param key: given key to search for
    :param tree: given radix tree to search
    :return: value
    """
    return find_node(key, tree).get()
