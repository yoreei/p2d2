#!/usr/bin/env python3

import ast
import astpp

def main():
#    with open("../workflows-mine/ba_max.py", "r") as source:
#        tree = ast.parse(source.read())
    tree = ast.parse(test1)

#    for node in ast.walk(tree):
#        #if isinstance(node, ast.FunctionDef):
#        #    print(node.name)
#        print(ast.dump(node)+'\n\n')
#
#        #node.body[-1]
    
    bytecode = compile(tree, '<string>', 'exec')
    exec(bytecode)


test1="""
#!/usr/bin/env python
import pandas as pd
import psycopg2

conn = psycopg2.connect("host=localhost dbname=tpch user=vagrant password=vagrant")

df = pd.read_sql_query("SELECT * FROM CUSTOMER", conn)
#df = pd.read_sql_table("customer", conn)
#breakpoint()
df = df["c_name"]
print (df)
"""

if __name__ == "__main__":
    main()
