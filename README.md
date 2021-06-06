# pyradixtree

This is a pure Python toy implementation of a radix tree, including a `MutableMapping` interface which can be used as follows:

```jupyterpython
>> from pyradixtree.mapping import RadixTreeMap
>> m = RadixTreeMap()
>> m['a'] = 1
>> m['abc'] = 3
>> del m['a']
>> len(m)
1
>> m['abc']
3
```

Note that for simplicity the key type is hardcoded to `str`.