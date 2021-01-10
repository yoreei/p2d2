# The problem with aggregations:

Pandas has a page in its documentation that is very helpful for us:

https://pandas.pydata.org/pandas-docs/stable/getting_started/comparison/comparison_with_sql.html

It is a direct comparison of SQL and Pandas with examples queries and their outputs. It shows us that Pandas and SQL have almost identical output format for GROUP BY operations:

```SQL
SELECT day, AVG(tip), COUNT(\*)
FROM tips
GROUP BY day;
/*
Fri   2.734737   19
Sat   2.993103   87
Sun   3.255132   76
Thur  2.771452   62
*/
```

```python
tips.groupby("day").agg({"tip": np.mean, "day": np.size})

#result:
#           tip  day
#day                
#Fri   2.734737   19
#Sat   2.993103   87
#Sun   3.255132   76
#Thur  2.771452   62
```

Also, with simpler syntax:
```python
df2.groupby('c_nationkey').max()

#result:
#             c_custkey  c_acctbal
#c_nationkey                      
#0               149917    9998.97
#1               149999    9994.84
#2               149998    9999.49
#3               149976    9998.32
```

This means that the conversion is easy. However, we also have to address non-grouped aggregations:

_1. agg without list_
```python
nogroup1 = df2.agg({'c_nationkey': np.sum, 'c_acctbal': np.max})

#result:
#c_nationkey    1801005.00
#c_acctbal         9999.99

#type Series
```

_2. agg with list_
```python
nogroup2 = df2.agg({'c_nationkey': [np.sum], 'c_acctbal': [np.max]})

#result
#                amax        sum
#c_nationkey      NaN  1801005.0
#c_acctbal    9999.99        NaN

#type DataFrame
```

_3. direct function call_
```python
df2.max() # possible parameters: axis, skipna, level, numeric_only

#result:
#c_custkey      150000.00
#c_nationkey        24.00
#c_acctbal        9999.99

#type Series
```

Above we see 3 ways to do the abstract equivalent to:

```sql
SELECT SUM(C_NATIONKEY) AS C_NATIONKEY, MAX(C_ACCTBAL) AS C_ACCTBAL
FROM CUSTOMER;
```

__The problem is the output format___. The sql query results in:

 c_nationkey | c_acctbal
-------------+-----------
     1801005 |   9999.99

None of Pandas' standard aggregation methods produce a result the same format as SQL. To overcome this, we should either:

1. Create an SQL query that mimics one of Pandas' formats (preferable but harder)

2. Force the user of the optimizer to use a specific syntax if they want their program optimized (going for this)

To accomplish 2) we will try to transform the output of method 1 (agg without list) or method 3 (direct function call) to the output of the SQL query. Notice that method 1 (agg without list) is more powerful because its interface allows to selectively map columns to aggregation functions, i.e. it is both a relational PROJECTION as well as an AGGREGATION. This is why, for the sake of simplicity, I prefer to proceed with method 3 (direct function call). Since our optimizer already supports PROJECTIONS, we do not lose the powerful functionality of method 1 (agg without list) since we can chain PROJECTIONs and simpler AGGREGATIONS.

_4 Cast and Transform in Pandas_

The next hurdle is the fact that Pandas makes a distinction between Series and DataFrames and SQL (afaik) works only with relations (tables), which are functionally and conceptionally closer to DataFrames. This means that whenever we encounter Series in our Pandas workflows we need to immediately transform it back to DataFrame, to keep the (intermediate) results closer to what is happening on the RDBMS front. Method 3 (direct function call) returns Series which can be transformed to a DataFrame using either of these methods:

```python
#sourced from https://stackoverflow.com/questions/40224319/pandas-series-to-dataframe-using-series-indexes-as-columns
df = pd.DataFrame(series).transpose()
df = pd.DataFrame([series])
df = series.to_frame().T
#note that .T is the same as .transpose()
```

We will use the last method of transforming Series to DataFrame because it is concise, readable and obious.

# Recap

_Syntax for GROUP BY aggregations_:

```python
#we could also use .agg but this syntax is simpler
df2.groupby('c_nationkey').max()
```

_Syntax for non-grouped (grand total) aggregations_:

```python
df2.max().to_frame().T
```

