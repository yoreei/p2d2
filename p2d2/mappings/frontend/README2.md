# How to write Backend to IR mappings

## Required fields

### Req

The following fields are required for every "req" entry:

```
"parenttype": str
"attrname": str
"kwarg_values": dict of str
"kwarg_types": dict of str
```

Additional fields are regarded as comments. The canonical way to provide a comment is through:

```
"__comment": str
```

### Maps

The following fields are required for every "maps" entry:

- ir: str
- modifies: str
- columns: str
- type: str

Additional field can be introduced, e.g. to provide additional information which will be required at in a later mapping. For example:

```
- "last_projection": "kwarg_values['key']",
- "original_columns": "__state[__parent_name]['columns']",
```

These are especially useful when a single operation cannot directly be mapped to the IR, but a sequence of operations can. In that case, the additional entries "bridge the gap" between the two mappings by providing some sort of state keeping.

## Special evaluation of fields

Fields in "req" do not undergo any evaluation and or substitution. Fields inside of "maps" undergo the following processes:

- ir: 
    1. String-formatted using Python's str.format(). See below for substition environment. This step is eager, i.e. it is performed as soon as the mapping is found to match
    2. Evaluated using Python's eval(). The same environment applies as for substitution. This step is lazy, i.e. it is performed when it is time to pull data from the database.
- modifies:
    1. Eagerly evaluated using Python's eval(). The same environment applies as above.
- columns: 
    1. Eagerly evaluated using Python's eval(). The same environment applies as above
- type: does not undergo substitutions and or evaluations

The reason for the double evaluation of __ir__ is so that we can extract the IR query after step 1 but before step 2. This is useful if the process needs to continue on another machine, since at that point the IR string is "self-sufficient". It is also useful for testing and debugging purposes.

## Evaluation and substitution environment. Access to state

In dictionary "maps", we have access to all data inside the "req" dictionary:

```
"parenttype": str
"attrname": str
"kwarg_values": dict of str
"kwarg_types": dict of str
```

Plus the following variables:
```
__state: dict
__parent_name: str
__kwarg_names: dict
__name
```

As well as all functions from the IR. This, combined with the fact that the "columns" entry is eagerly evaluated, can be used to fetch columns from the backend for libraries that do not state them explicitly. See the example implementation


### Examples:

#### Get ```'mask_operand'``` of argument 'key':
```
__state[__kwarg_names['key']]['mask_operand']
```

#### Get ```'series_column'``` of parent:

```
__state[__parent_name]['series_column']
```

