This folder contains various mutators on a radix tree. 

The following operations are supported and all mutate a given radix tree of type `Node[T]`, where `T` is an arbitrary type:

* `modify` given a `key` and a new `value`, find the `key` if it exists and replace its value with `value`. The key must exist in the tree, so the radix tree structure does not need to be changed.
* `insert` given a `key` and a `value`. The key must not exist in the tree, so the radix tree may require structural changes to preserve its definition.
* `delete` given `key`. As with `insert` this may require structural changes to the tree to preserve its definition.

The following operations do not mutate the tree:
* `length` gives the number of items stored
* `find` finds the item in the tree and returns its value.
