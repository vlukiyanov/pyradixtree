from typing import List, Optional, Tuple, TypeVar

from pyradixtree.node import Node, Sentinel
from pyradixtree.operations._find import _compare_find

T = TypeVar("T")


def delete(key: str, tree: Node[T]) -> Optional[str]:
    """
    Remove key from radix tree, tidying up any dangling nodes to preserve the
    tree property; returns removed key.

    :param key: given key to remove
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
                current_root = path[-1]
                current_root.children.remove(item)
                if len(path) >= 2 and len(current_root.children) == 1:
                    current_child = current_root.children[0]
                    current_root.children = current_child.children
                    current_root.key = current_root.key + current_child.key
                    current_root.value = current_child.value
                return key
            else:
                # found a prefix, focus search
                path.append(item)
                acc = [(node, comparison) for node in item.children]
    return None
