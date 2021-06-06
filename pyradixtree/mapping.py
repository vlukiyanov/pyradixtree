from typing import Iterator, List, MutableMapping, TypeVar

from pyradixtree.node import Node, Sentinel
from pyradixtree.operations import delete, find, insert, length

VT = TypeVar("VT")


class RadixTreeMap(MutableMapping[str, VT]):
    def __init__(self):
        self._root: Node[VT] = Node(key=None, value=Sentinel.MISSING, children=[])

    def __setitem__(self, k: str, v: VT) -> None:
        insert(k, v, self._root)

    def __delitem__(self, v: str) -> None:
        delete(v, self._root)

    def __getitem__(self, k: str) -> VT:
        return find(k, self._root, return_path=False)[0]

    def __len__(self) -> int:
        return length(self._root)

    def __iter__(self) -> Iterator[str]:
        acc: List[Node[VT]] = [self._root]
        while acc:
            item = acc.pop()
            acc.extend(item for item in item.children)
            if item.value is not Sentinel.MISSING:
                yield item.key  # type: ignore

    def __repr__(self):
        return repr(dict(self.items()))
