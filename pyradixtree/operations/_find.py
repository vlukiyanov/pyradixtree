from itertools import zip_longest
from typing import List, Optional, Tuple, TypeVar

from pyradixtree.node import Node, Sentinel

T = TypeVar("T")


def _compare_find(search: str, prefix: Optional[str]) -> Optional[str]:
    """
    Helper function for find, checks whether the prefix should be explored
    for further search.
    """
    acc: List[str] = []
    if prefix is None:
        return None
    for (s, p) in zip_longest(search, prefix):
        if s is None:
            # search is shorter than prefix
            return None
        elif p is None:
            # search is longer than prefix, but contains prefix
            acc.append(s)
        elif s == p:
            continue
        else:
            return None
    return "".join(acc)


def find(key: str, tree: Node[T], return_path: bool = True) -> Tuple[T, List[Node[T]]]:
    """
    Find and return the value and path to a given

    :param key: given key to search for
    :param tree: given radix tree to search
    :param return_path: whether to return path, default True
    :return: tuple of value and path if found, otherwise KeyError is raised; if the
        return_path is set to False then the returned path is always empty
    """
    path: List[Node[T]] = []
    acc: List[Tuple[Node[T], str]] = [(tree, key)]
    while acc:
        item, search = acc.pop()
        if item.is_root:
            if return_path:
                path.append(item)
            acc.extend((node, search) for node in item.children)
        else:
            comparison = _compare_find(search, item.key)
            if comparison is None:
                # item not found, continue looking through acc
                continue
            elif comparison == "" and item.value != Sentinel.MISSING:
                # found the exact item, return it
                if return_path:
                    path.append(item)
                return item.get(), path
            else:
                # found a prefix, focus search
                if item.key == "":
                    continue
                if return_path:
                    path.append(item)
                acc = [(node, comparison) for node in item.children]
    # if we exhaust search without finding a prefix or the exact item, we end up here
    raise KeyError()
