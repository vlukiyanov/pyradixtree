from typing import List, TypeVar

from pyradixtree.node import Node, Sentinel

T = TypeVar("T")


def length(tree: Node[T]) -> int:
    """
    Count the number of items in a radix tree.

    :param tree:
    :return: number of items
    """
    counter: int = 0
    acc: List[Node[T]] = [tree]
    while acc:
        item = acc.pop()
        acc.extend(item for item in item.children)
        if item.value is not Sentinel.MISSING:
            counter += 1
    return counter
