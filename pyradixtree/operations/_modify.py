from typing import List, Optional, Tuple, TypeVar

from pyradixtree.node import Node, Sentinel
from pyradixtree.operations._find import _compare_find

T = TypeVar("T")


def modify(key: str, value: T, tree: Node[T]) -> Optional[str]:
    """
    Modify the given value to a key, returning the key if this succeeds.

    :param key: given key to modify
    :param value: given value to modify to
    :param tree: given radix tree
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
            if comparison is None:
                continue
            elif comparison == "" and item.value != Sentinel.MISSING:
                # found the item, modify it
                item.value = value
                return key
            else:
                # found a prefix, focus search
                path.append(item)
                acc = [(node, comparison) for node in item.children]
    return None