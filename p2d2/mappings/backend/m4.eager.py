"""
This is part of the backend implementation.

"""
from p2d2.IRBuilder.db_abc import DB_ABC
import psycopg2

    
def __FETCH_COLUMNS(query:str, connstr:str)->list:
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    src_query = resolve(name, lineno)
    cur.execute(f"create or replace temp view p2d2_check_cols as {src_query}")
    cur.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name='p2d2_check_cols'"
    )
    colnames_nested = cur.fetchall()  # nested like [('c_custkey'),('c_acctbal)]
    cur.close()
    conn.close()
    return [
        item for sublist in colnames_nested for item in sublist
    ]  # unnests, like ['c_custkey'..]
