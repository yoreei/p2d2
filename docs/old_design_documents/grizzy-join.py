import grizzly
from grizzly.aggregates import AggregateType
from grizzly.sqlgenerator import SQLGenerator
from grizzly.relationaldbexecutor import RelationalExecutor
import psycopg2

conn = psycopg2.connect(f'host=localhost dbname=tpch user=vagrant password=vagrant')
grizzly.use(RelationalExecutor(conn, SQLGenerator('sqlite')))

df1 = grizzly.read_table('orders') 
df1 = df1[['o_custkey', 'o_orderstatus']]
df2 = grizzly.read_table('customer')
df2 = df2[['c_custkey', 'c_acctbal']]
joined = df1.join(other = df2, on=['o_custkey', 'c_custkey'], how = 'inner')
print(joined.generateQuery())
joined.show(pretty=True)

grizzly.close()
