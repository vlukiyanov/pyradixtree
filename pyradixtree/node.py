import dataclasses
import enum
from typing import Generic, List, MutableSequence, Optional, TypeVar, Union

T = TypeVar("T")


class Sentinel(enum.Enum):
    MISSING = object()


@dataclasses.dataclass(frozen=False)
class Node(Generic[T]):
    key: Optional[str]
    children: MutableSequence["Node[T]"]
    value: Union[T, Sentinel]

    @property
    def is_leaf(self) -> bool:
        return self.value is not Sentinel.MISSING

    @property
    def is_root(self) -> bool:
        return self.key is None

    def get(self) -> T:
        if not self.is_leaf:
            raise KeyError()
        else:
            return self.value  # type: ignore


def pretty_path(l: List[Node[T]]) -> str:
    acc: List[str] = []
    for item in l:
        if item.key is None:
            acc.append("{Root}")
        else:
            acc.append(item.key)
        if not item.is_leaf:
            acc.append(" -> ")
    return "".join(acc)
