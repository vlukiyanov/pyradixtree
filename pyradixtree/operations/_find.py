from itertools import zip_longest
from typing import List, Optional, Tuple, TypeVar

from pyradixtree.node import Node, Sentinel

T = TypeVar("T")


# TODO better sentinel handling


def _compare_find(search: str, prefix: Optional[str]) -> Optional[str]:
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


def find(key: str, tree: Node[T]) -> Tuple[T, List[Node[T]]]:
    path: List[Node[T]] = []
    acc: List[Tuple[Node[T], str]] = [(tree, key)]
    while acc:
        item, search = acc.pop()
        if item.is_root:
            path.append(item)
            acc.extend((node, search) for node in item.children)
        else:
            comparison = _compare_find(search, item.key)
            if comparison is None:
                # item not found, continue looking through acc
                continue
            elif comparison == "" and item.value != Sentinel.MISSING:
                # found the exact item, return it
                path.append(item)
                return item.get(), path
            else:
                # found a prefix, focus search
                if item.key == "":
                    continue
                path.append(item)
                acc = [(node, comparison) for node in item.children]
    # if we exhaust search without finding a prefix or the exact item, we end up here
    raise KeyError()
