# pyradixtree

This is a pure Python toy implementation of a radix tree, including a `MutableMapping` interface which can be used as follows:

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

Note that for simplicity the key type is hardcoded to `str`. Another limitation is keys must have length greater than 0, or equivalently that `""` is not allowed as a key.

The package can be installed using `poetry` for development, see for instructions at https://python-poetry.org/docs/ to install `poetry` itself. Once installed you can run the tests using `poetry run pytest`.

This was created as a playground for learning the excellent `hypothesis` library.