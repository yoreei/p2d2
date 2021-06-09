import uuid

def _wrapas(sql):
    return f'({sql}) AS {uuid.uuid1()}'

def __columns():
    return NotImplemented

def commit(sql):
    return sql+';'

def LIMIT(num, source):
    return f'SELECT * FROM {_wrapas(source)} LIMIT {num}'

def PROJECTION(cols: list, source: str):
    return f"SELECT {', '.join(cols)} FROM {_wrapas(source)}"
    
def DBSOURCE(table_name:str):
    return f"SELECT * FROM {table_name}"

def SELECTION(condition: str, source: str):
    return f"SELECT * FROM {_wrapas(source)}"

def JOIN(right:str, how:str, on:str, source:str):
    return f"SELECT * FROM {_wrapas(source)} {how} JOIN {right} ON {on}"

def MIN(by:(str or list), source:str):
    by = list(by) # make sure by is a list
    to_min = __columns() - by
    minfunc = lambda x: f'MIN({x})'
    minfuncs = map(minfunc, to_min) # ['MIN(col1)', 'MIN(col2)']
    
    return f'SELECT {", ".join(minfuncs)} FROM {_wrapas(source)} GROUP BY {by}'

def MAX(by:(str or list), source:str):
    by = list(by) # make sure by is a list
    to_min = __columns - by
    minfunc = lambda x: f'MIN({x})'
    minfuncs = map(minfunc, to_min) # ['MIN(col1)', 'MIN(col2)']
    return f"SELECT {', '.join(minfuncs)} FROM {_wrapas(source)} GROUP BY {', '.join(by)}"

    
