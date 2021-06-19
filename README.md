# pyradixtree

This is a pure Python toy/experimental implementation of a radix tree, including a `MutableMapping` interface which can be used as follows:

```python
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

Note that for simplicity the key type is hardcoded to `str`; another limitation is keys must have length greater than 0, so `""` is not allowed as a key. 

This was created as a playground for learning the excellent `hypothesis` library.