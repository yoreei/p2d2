# How to write Backend to IR mappings

## Required fields

Please, refer to the example implementation

## Access to state

In dictionary "maps", we have access to the following information:

```
__state: dict
__parent_name: str
__kwarg_names: dict
__name
```

As well as all data inside the "req" dictionary, with the exception of the "```__comment```" entry:

```
parenttype: str
attrname:str
kwarg_values:dict
kwarg_types:dict
parent_state:list
kwarg_values: dict
```


### Examples:

#### Get ```'mask_operand'``` of argument 'key':
```
__state[__kwarg_names['key']]['mask_operand']
```

#### Get ```'series_column'``` of parent:

```
__state[__parent_name]['series_column']
```

#### Get 
