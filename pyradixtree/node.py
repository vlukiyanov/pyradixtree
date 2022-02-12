import dataclasses
import enum
from typing import Generic, MutableSequence, Optional, TypeVar, Union

T = TypeVar("T")


class Sentinel(enum.Enum):
    MISSING = object()


@dataclasses.dataclass(frozen=False)
class Node(Generic[T]):
    """
    The radix tree is made up of nodes which are represented in this dataclass, with the key the
    string.

    Not all nodes store values, those which do will have value of type T, those that do
    not will have value set to Sentinel.MISSING.
    """

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
        # only leaves have values
        if not self.is_leaf:
            raise KeyError()
        else:
            return self.value  # type: ignore
