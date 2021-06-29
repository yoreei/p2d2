import uuid
# from p2d2.IRBuilder.irfunctions import __columns

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

def STATIC_SELECTION(column, operator, operand, condition: str, source: str):
    return f"""
            SELECT * FROM {_wrapas(source)}
            WHERE {column} {operator} {operand}
            """

def DYNAMIC_SELECTION(column, operator, operand, condition: str, source: str):
    return f"""
            SELECT * FROM {_wrapas(source)}
            WHERE {column} {operator} ({DBSOURCE(operand)})
            """

def JOIN(right:str, how:str, on:str, source:str):
    return f"SELECT * FROM {_wrapas(source)} {how} JOIN {right} ON {on}"

def COUNT_VALUES(column:list, values_col:str, count_col:str, source:str):
    return f'SELECT {column} AS {values_col}, COUNT(*) AS {count_col} FROM {_wrapas(source)} GROUP BY {column}'

def DROPNA(cols: list, source:str):
    dropfunc = lambda x: f'{x} IS NOT NULL'
    drops = list(map(dropfunc, cols))

    return f"SELECT * FROM {_wrapas(source)} WHERE {' AND '.join(drops)}"

def ISIN(col: list, values:object, source:str):
    if isinstance(values, str):
        inlist = values
    elif isintance(values, list):
        inlist = _list2cols(values)

    return f"""
        SELECT * FROM {_wrapas(source)}
        WHERE {col} IN ({values})
    """
    
def CASE(column:str, to_replace:str, value:str, all_columns:list, source:str):
    rest_cols = list(set(all_columns) - {column})
    return f"""
    SELECT    
        CASE
            WHEN {column} = {to_replace} THEN {value}
        END AS "{column}",
        {_list2cols(rest_cols)}
    FROM {_wrapas(source)}
    """
        
