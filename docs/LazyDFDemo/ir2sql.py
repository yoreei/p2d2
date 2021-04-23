import uuid

def _wrapas(sql):
    return f'({sql}) AS {uuid.uuid1()}'

def commit(sql):
    return sql+';'

def LIMIT(num, source):
    return f'SELECT * FROM {_wrapas(source)} LIMIT {num}'

def PROJECTION(cols: list, source: str):
    return f"SELECT {', '.join(cols)} FROM {_wrapas(source)}"
    
    