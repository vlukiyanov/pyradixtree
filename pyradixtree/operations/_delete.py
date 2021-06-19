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
    acc: List[Tuple[Node[T], str, List[Node[T]]]] = [(tree, key, [])]
    while acc:
        item, search, path = acc.pop()
        if item.is_root:
            acc.extend((node, search, path + [item]) for node in item.children)
        else:
            comparison = _compare_find(search, item.key)
            if comparison is None:
                # item not found, continue looking through acc
                continue
            elif comparison == "" and item.is_leaf:
                # found the item, modify it
                current_root = path[-1]
                current_root.children.remove(item)
                if len(path) >= 2 and len(current_root.children) == 1:
                    current_child = current_root.children[0]
                    current_root.children = current_child.children
                    current_root.key = current_root.key + current_child.key  # type: ignore
                    current_root.value = current_child.value
                return key
            else:
                acc.extend((node, comparison, path + [item]) for node in item.children)
    return None
