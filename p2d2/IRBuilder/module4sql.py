import uuid
from p2d2.IRBuilder.irfunctions import __columns

def _wrapas(sql):
    return f'({sql}) AS {uuid.uuid1()}'

def _list2cols(l:list):
    """
    Fixes the case if a column has a keyword name
    """
    return '"'+'", "'.join(l)+'"'

def commit(sql):
    return sql+';'

def PROJECTION(cols: list, source: str):
    return f"SELECT {', '.join(cols)} FROM {_wrapas(source)}"
    
def DBSOURCE(table_name:str):
    return f"SELECT * FROM {table_name}"

def SELECTION(condition: str, source: str):
    return f"SELECT * FROM {_wrapas(source)}"

def JOIN(right:str, how:str, on:str, source:str):
    return f"SELECT * FROM {_wrapas(source)} {how} JOIN {right} ON {on}"

def COUNT(by:list, as:str, source:str):
    return f'SELECT {", ".join(by)}, COUNT(*) FROM {_wrapas(source)} GROUP BY {", ".join(by)}'

def DROPNA(cols: list, source:str):
    dropfunc = lambda x: f'{x} IS NOT NULL'
    drops = list(map(dropfunc, cols))

    return f"SELECT * FROM {_wrapas(source)} WHERE {' AND '.join(drops)}"

def ISIN(col: list,  source:str):
    


