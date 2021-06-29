"""
This is part of the backend implementation.
"""
from p2d2.IRBuilder.db_abc import DB_ABC
import psycopg2

def __ESTABLISH_CONNECTION(host:str, db:str, username:str, password:str)->None:
    
def __FETCH_COLUMNS_QUERY(query:str)->list:
    return 

def __FETCH_COLUMNS_TABLE(table:str)->list:
    NotImplemented

def __REGISTER_DBSOURCE(module:str, attrname:str, query_arg:str, con_arg:str)->None:
    

def EVAL_QUERY(self, query):
    pass
    
def EXEC_QUERY(self, query)->None:
    pass
