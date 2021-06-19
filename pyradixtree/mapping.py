from typing import Iterator, List, MutableMapping, Tuple, TypeVar

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
        return find(k, self._root)

    def __len__(self) -> int:
        return length(self._root)

    def __iter__(self) -> Iterator[str]:
        acc: List[Tuple[Node[VT]]] = [(self._root,)]
        while acc:
            item = acc.pop()
            for child in item[-1].children:
                acc.append(item + (child,))  # type: ignore
            if item[-1].value is not Sentinel.MISSING:
                yield "".join(i.key for i in item if i.key is not None)  # type: ignore

    def __repr__(self):
        return repr(dict(self.items()))
