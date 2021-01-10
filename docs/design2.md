# Design v2

## Why start again?

Two reasons:

- The structures (read, classes) of Design v1 were aimed to completely overtake the codetree by wrapping around the original Python classes. The rationale was that the original Python classes do not provide the information that the optimizer needs while also bringing a lot of "unneeded clutter". However, during the implementation of Design v1, the classes of the optimizer started to look more and more like the stock classes they were supposed to mask - a lot of what I previously considered "clutter" started to seem useful. 

- The implementation of Design v1 made me familiar with the workings of the `ast` module - I now have my opinions of when it is advantageous to use the tools provided by the `ast` module and when it's better to "roll your own". In hindsight, the implementation of Design v1 was the opposite of optimal in this regard.

## Step 1: the creation of "nodedict"

Nodedict is supposed to store the ids of variable and the SQL which generates these variables:
SELECT * FROM (SELECT * FROM) AS q1
```python
nodedict = {
    "a" : {
        1 : {
            "sql" : "(SELECT * FROM customer ) as a1",
            "unresolved : None,},
        2: {
            "sql" : "(SELECT c_acctbal FROM {} AS a2 )",
            "unresolved" : ['a', ,},
        },
    "b" : {
        3: {
            "sql" : "(SELECT * FROM {} WHERE c_acctbal > 500 AS b3)",
            "unresolved" : 'a',},
     
        } 
}

```

Use .format to nest queries
.format crashcourse:

```python
formatme='hi {}'
return formatme.format('bob')
# returns 'hi bob'
```

# Problems

## The join problem:

Pandas' joins and SQLs joins behave differently. Example SQL join:
```sql
SELECT *
FROM
    (SELECT O_ORDERSTATUS, O_CUSTKEY
    FROM ORDERS) AS t1
INNER JOIN
    (SELECT C_CUSTKEY, C_ACCTBAL
    FROM CUSTOMER) AS t2
ON O_CUSTKEY=C_CUSTKEY;

```
The result:


 o_orderstatus | o_custkey | c_custkey | c_acctbal
---------------+-----------+-----------+----------
 F             |     55624 |     55624 |    818.33
 O             |    124828 |    124828 |   6629.21
 O             |     28547 |     28547 |   2095.42
 F             |     84487 |     84487 |   -659.55
 O             |     29101 |     29101 |   2261.04

And the "equivalent" pandas code:


```python

import pandas as pd
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=tpch user=vagrant password=vagrant")

df1 = pd.read_sql_query('SELECT * FROM orders', conn)
df2 = pd.read_sql_query('SELECT * FROM customer', conn)
df1 = df1[['o_orderstatus','o_custkey']]
df2 = df2[['c_custkey', 'c_acctbal']]

joined = df1.join(other = df2.set_index('c_custkey'), on='o_custkey', how = "inner")
print(joined)

```
The result:


       |o_orderstatus| o_custkey| c_acctbal
-------|-------------|----------|----------
0      |            O|     36901|   4809.84
45920  |            F|     36901|   4809.84
140227 |            F|     36901|   4809.84
239018 |            F|     36901|   4809.84
293029 |            O|     36901|   4809.84
...    |          ...|       ...|       ...


Notice the number of named columns:

SQL: o_orderstatus | o_custkey | c_custkey | c_acctbal
pandas: o_orderstatus| o_custkey| c_acctbal

SQL retains the duplicate columns on which we performed the join. One way I found around this is to avoid "the evil \*" and to explicitly SELECT all column without the duplicate one (e.g.:

```sql

SELECT O_ORDERSTATUS, O_CUSTKEY, C_ACCTBAL
FROM
    (SELECT O_ORDERSTATUS, O_CUSTKEY
    FROM ORDERS) AS T1
INNER JOIN
    (SELECT C_CUSTKEY, C_ACCTBAL
    FROM CUSTOMER) AS T2
ON O_CUSTKEY=C_CUSTKEY;

```

*But this requires that we know the names of all the columns*. This is not always the case, e.g. when optimizing this pandas workflow:

```python
df1 = pandas.read_sql('SELECT * FROM CUSTOMER'..)
df2 = pandas.read_sql('SELECT * FROM ORDERS'..)
joined = df1.join(other = df2.set_index('c_custkey'), on='o_custkey', how='inner')
```

Since the data scientist never performed a Projection on the dataframes, the python program simply does not containinformation about the columns. All we know is that the column 'c_custkey' and 'o_custkey' exist, but this is not enough for the SELECT statement, which requires explicit listing of the columns that should be included.

### Solution 1: use VIEW

I don't know enough about views but:

```sql
CREATE VIEW J1 AS:
SELECT *
FROM
    (SELECT O_ORDERSTATUS, O_CUSTKEY
    FROM ORDERS) AS T1
INNER JOIN
    (SELECT C_CUSTKEY, C_ACCTBAL
    FROM CUSTOMER) AS T2
ON O_CUSTKEY=C_CUSTKEY;
```

And then (this probably won't work, but hopefully there is some way to accomplish the idea):


```sql
ALTER VIEW J1
DROP COLUMN C_CUSTKEY;
```

Basically what we did was: we joined both tables using the "sql" way, which results in the additional column, we saved the query as a VIEW and we modified the VIEW so that the additional column is removed.

#### Caveat

If this is possible, there is an edge case problem: what if the columns we join on have the same name? In our previous example from the TCPH database, we joined on O_CUSTKEY=C_CUSTKEY, but if both the ORDERS table and the CUSTOMER table had a column named CUSTKEY (without the prefix) then the view J1 (from the previous example) would contain the following columns:

ORDERSTATUS | CUSTKEY | CUSTKEY | ACCTBAL

and that would make the ```DROP COLUMN CUSTKEY``` query abiguous.

#### Caveat solution 1

We have to rename the columns of the subqueries before joining, to ensure that they have unique names. Since we don't want to alter the database, we could probably use VIEWs again and rename the columns of the views. Again, this might not be possible if we don't know the exact names of the tables (because they aren't contained in the python program)

#### Caveat solution 2

Or, we could assume that all columns are unique througout the whole database, which is the case for the TCPH database and seems like good practice anyway?

### Solution 2: use TEMP TABLE

If VIEWS can't drop their columns after creation, then TABLEs certainly can. Using tables might degrade performance

### Solution 3: Query the column names in the python runtime

If we assume that the optimizer has access to the database, then we can write an SQL join query which mimicks Pandas behaviour (dropping the duplicate column). We need to query the column names of the tables we are joining, remove the duplicate column and only then construct our join query. Like this:

```python
def construct_join_query(table1, table2, left_on, right_on):

    columns1 = pandas.read_sql(f'SELECT column_name FROM information_schema.column WHERE table_name="{table1}"..)
    columns2 = pandas.read_sql(f'SELECT column_name FROM information_schema.column WHERE table_name="{table2}"..)
    
    # create a set of the columns of table1 and table2, without the duplicate column in table 2
    all_columns = set(columns1) + set(columns2) - set([right_on])

    return f"""\
SELECT {all_columns}
FROM
    (SELECT O_ORDERSTATUS, O_CUSTKEY
    FROM ORDERS) AS T1
INNER JOIN
    (SELECT C_CUSTKEY, C_ACCTBAL
    FROM CUSTOMER) AS T2
ON O_CUSTKEY=C_CUSTKEY;
"""

#### Caveat

Solution 3 introduces 2 additional database pulls per join (assuming a simple 2-table join). As we know from "Don't hold my data hostage" these pulls could be costly. Luckily, we can rerwrite the construct_join_query function to only use 1 pull (regardless of how many tables we are joining). 

#### Caveat solution

```python
all_columns = pandas.read_sql("""
SELECT column_name FROM information_schema.columns WHERE table_name='orders' 
UNION
SELECT column_name FROM information_schema.columns WHERE table_name='customer' AND column_name!='c_custkey' 
;
"""

    return f"""\
SELECT {all_columns}
...
```

We could further optimize this to use 0 additional pulls if we take advantage of PL/Python and create a pandas_join function which would look a lot like the "caveat solution" code, with the advantage that the pandas_join function will be run entirely in Postgres. It makes sense not to count the definition of the function inside Postgres as part of the query execution time when benchmarking, because this function is a "requirement" for our optimizer to run.
However, I've never used PL/Python, so the other solutions could probably be implemented faster.


### But how does grizzly do it?

tldr: Grizzly cheats

The following Grizzly program does performs the same operations with the same data as the pandas program described in the subsection "the join problem". However, it returns the same result as the *SQL* program:

```python
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
```

The result:

```sql
SELECT * FROM (SELECT _t1.o_custkey,_t1.o_orderstatus FROM (SELECT * FROM orders _t0) _t1) _t7 inner JOIN (SELECT _t3.c_custkey,_t3.c_acctbal FROM (SELECT * FROM customer _t2) _t3) _t8 ON _t7.o_custkey = _t8.c_custkey
```

 o_custkey | o_orderstatus | c_custkey | c_acctbal
   55624   |       F       |   55624   |  818.33
  124828   |       O       |  124828   |  6629.21
   28547   |       O       |   28547   |  2095.42
   84487   |       F       |   84487   |  -659.55
   29101   |       O       |   29101   |  2261.04
   71134   |       F       |   71134   |  398.12
....

So, to compare directly, when joining 2 tables with 2 columns each on 1 column, the resulting table has the following columns:
SQL: o_custkey | o_orderstatus | c_custkey | c_acctbal 
pandas: o_orderstatus| o_custkey| c_acctbal
Grizzly: o_custkey | o_orderstatus | c_custkey | c_acctbal 

We can see that Grizzly performs a standard SQL join, so the result is unsurprising. Grizzly is not a drop-in Pandas replacement but I think this is a poor defence: Since Grizzly targets Pandas users, said users would have a hard time figuring "gotchas" such as the one described here.

### Why not emulate SQL behaviour with Pandas?

In other words, why not find some (perhaps not as popular / standard) Pandas syntax that behaves like SQL and "assume" that our workflows will use that for the thesis?

- People who write SQL themselves do not use SELECT * when joining

