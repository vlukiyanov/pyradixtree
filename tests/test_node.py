from pyradixtree.node import Node, Sentinel


def test_mutation():
    subtree = Node(key="ab", value=Sentinel.MISSING, children=[])
    tree = Node(key=None, value=Sentinel.MISSING, children=[subtree])
    subtree.key = "cd"  # would throw if the dataclass is marked frozen
    assert tree.children[0].key == "cd"
