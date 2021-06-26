# Design Decisions

## Pandas' surprises

To understand the following design decisions, lets look at some surprises Pandas has for us.

## Pandas' slice and dice

First, there are many ways to sllice and dice a DataFrame in Pandas: df[], df.loc[], df.iloc[] as well as some deprecated or outright inconsistent methods which do not deserve mentioning. Of the three mentioned, df.loc and df.iloc will be used because they have the most explicit syntax: 
https://stackoverflow.com/questions/38886080/python-pandas-series-why-use-loc/38886211#38886211

## Pandas' views

Let's create a projection:

```python
proj = df.loc[:,'c_acctbal'] # take a column from df

proj._is_view

>> True
```

proj is usually (but not always, this depends on conditions which pandas has no control over) a View of df, which means that any changes in df will be reflected on proj and any(most?) changes in proj will be reflected on df. And now this example:

To guard users from manipulating a view while believing it is a copy, Pandas will sometimes issue a SettingWithCopyWarning:

```python
proj = df.loc[:, 'c_acctbal'] # by far the most used syntax after df[..]

proj.loc[0:2]=100 # manipulation probably changes the original df too

>>SettingWithCopyWarning
```

Pandas usually (but not always) raises this warning because it does not like you manipulating potential views, it is apparently considered a bad practice. We assume that our input programs are well-written, so we can enforce strictness with:

```
pd.set_option('mode.chained_assignment','raise')
```

This will raise an exception in the above example. However, sometimes the exception is not raised:

```python
z = pd.DataFrame([[11,12,13],[21,22,23],[31,32,33]]
y = z.iloc[:,0] # take column [11,12,13]
y.iloc[2]=500
```

But we are not done with views yet:

```python
proj = df.loc[:, 'c_acctbal'] # by far the most used syntax after df[..]

df.loc[0:2, 'c_acctbal']=100 # changes are probably reflected in proj 
```

This raises no errors so Pandas believes this to be good code, even though it is still ambiguous (we should embrace undeterministic programming languages). The value of proj will be different depending on if proj happened to be a view (most cases, but not guaranteed) or a copy. And this is not a corner case example, this is the typical pandas code you see on kaggle and stackoverflow (with the slight difference that the more finnicky df[] is more popular there, but the problem of views vs copies still exists.)

### Whether a view or a copy is created depends on the data

```python
import pandas as pd
import io

def df_is_view(datastr:str):
    data = pd.read_csv(datastr, sep='|')

    rows = data.iloc[0:3]
    print (f'rows slice is view? {rows._is_view}')
    cols = data.iloc[:,1]
    print (f'col slice is view? {cols._is_view}')

customer_str=io.StringIO("""
1|Customer#000000001|IVhzIApeRb ot,c,E|15|25-989-741-2988|711.56|BUILDINGto the even, regular platelets. regular, ironic epitaphs nag e
2|Customer#000000002|XSTf4,NCwDVaWNe6tEgvwfmRchLXak|13|23-768-687-3665|121.65|AUTOMOBILE|l accounts. blithely ironic theodolites integrate boldly: caref
3|Customer#000000003|MG9kdTD2WBHm|1|11-719-748-3364|7498.12|AUTOMOBILE| deposits eat slyly ironic, even instructions. express foxes detect slyly. blithely even accounts abov
4|Customer#000000004|XxVSJsLAGtn|4|14-128-190-5944|2866.83|MACHINERY| requests. final, regular ideas sleep final accou
5|Customer#000000005|KvpyuHCplrB84WgAiGV6sYpZq7Tj|3|13-750-942-6364|794.47|HOUSEHOLD|n accounts will have to unwind. foxes cajole accor
6|Customer#000000006|sKZz0CsnMD7mp4Xd0YrBvx,LREYKUWAh yVn|20|30-114-968-4951|7638.57|AUTOMOBILE|tions. even deposits boost according to the slyly bold packages. final accounts cajole requests. furious
""")

name_address_str = io.StringIO("""
Customer#000000001|IVhzIApeRb ot,c,E
Customer#000000002|XSTf4,NCwDVaWNe6t
Customer#000000003|MG9kdTD2WBHm111
Customer#000000004|XxVSJsLAGtn414-
Customer#000000005|KvpyuHCplrB84WgAi
Customer#000000006|sKZz0CsnMD7mp4Xd0
Customer#000000007|TcGe5gaZNgVePxU5k
""")

id_address = io.StringIO("""
1|IVhzIApeRb ot,c,E
2|XSTf4,NCwDVaWNe6t
3|MG9kdTD2WBHm111
4|XxVSJsLAGtn414-
5|KvpyuHCplrB84WgAi
6|sKZz0CsnMD7mp4Xd0
7|TcGe5gaZNgVePxU5k
""")

df_is_view(customer_str)
df_is_view(name_address_str)
```

Output:

```
rows slice is view? False
col slice is view? True
rows slice is view? True
col slice is view? True
rows slice is view? False
col slice is view? True
```

As we can see, USUALLY, using iloc with a range (iloc[0:3]) produces a copy, whereas integers produce a view (iloc[:,1]). However, example 2 shows us it all depends on the data. Some experimenting suggests that this happens if all the columns are of the same type (in example 2 both are of type 'object' ie. a string).

To top it off, loc and iloc have different views on the matter of views:

```python
vv = a.loc[:, 'c_acctbal':'c_acctbal'] # view
vi = a.iloc[:, 0:0] # copy
```

### Relational selection can be done only with this syntax: .loc[condition]

```python
sel = a.loc[a.loc[:,'custkey']<5]
sel._is_view # False
```

Which is similar to SQL: `WHERE custkey < 5`
My own testing and Stackoverflow suggest that .loc[.loc[condition]] will always return a copy.

### Relational projection can be done only with indexes

```python
proj = a.iloc[:, 0] # view
projc= a.iloc[:, 0:0] # copy
```

But this is useless to us because we are working with an RDBMS

### Conclusion

We have no realiable way of controlling if a view or a copy is created in a relational projection. We have several possibilities:
- 1 Mimick Pandas' behaviour by executing the program during the optimization step is also out of the question, because a compiled program is set in stone, but data can change. It makes no sense to assume that the data will be the same after compilation or even that we have access to the data during compilation. 
- 2 We could simply ignore any workflows that use loc, iloc and [] but those are probably the top most used operators in Pandas. 
- 3 We could forbid any mutating operations on dataframes that have potential views as well as on the views themselves, unless a .copy() is explicitly called. 
- 4 We could treat everything as a copy and thus break pandas compatibility. Going with this for now

## Data types: tbls and vars

When this document (and the code) speaks of 'itbl_{name}' (short for intermediate table), it means data generated from a query inside the DBMS. This is to distinguish between tbl (a persistent table in the RDBMS) and the intermediate results from queries. 'var_{name}' represents variable inside the Python runtime. A Pull() node's job is to download an *itbl* into a *var* for consumption by unsupported operations (called Actions).

## Optimization stages (Representations)

Beyond the python AST and the bytecode representations, we have 3 intermediate representations. To illustrate the following representations, this Python code will be transormed into each of them:

import pandas as pd
import pgconn
conn = pgconn.get() #gives us a connection to PostgreSQL. 
a = pd.read_sql_query('SELECT * FROM customer', conn)
b = a.loc[:,['c_custkey','c_name','c_acctbal']] # we assume a projection is always a copy
c = b.loc[a.loc[:,'c_acctbal']<800] # selections seem to be a copies
a.loc[a['c_acctbal'] < 800, 'c_acctbal'] = 4 #inPlace
machineLearningAlgorithm(a)

### 1. Procedural Representation (PR)

PR is the closest to the python AST. It is achieved simply by replacing `ast` Nodes which represent supported operations with custom `nodes` which take their names from relational algebra: Selection, Projection, Join to name a few. Simplified example:

```python
Assign(tar = tbl_a, src = DBTable(tbl='customer', conn=conn)
Assign(tar = tbl_b, src = Projection(cols = ['c_custkey', 'c_name', 'c_acctbal'], src = tbl_a))
Assign (tar = tbl_c, src = Selection (cols = ['acctbal'], cond = '<800', src = tbl_b)
Assign (tar = tbl_a, inPlace=True, src = Update (sel = Selection(..), proj = Proj(..), op = '=4' src = tbl_a),
Pull(tar= 'var_b', src = tbl_b),
Action(dependency = 'var_b'),
Pull(tar= varname2, src = tbl_a),
Action(dependency = 'var_a'),
Ignored(),
Ignored(),
...
```

Notice how tbl_a is mutable.

#### Note on Views:

 var_b would also be muted, because it is a View of tbl_a.

#### Available Nodes (PR):

**IO:**

    DBSource
    Pull
    Action

**Relational:**

    Selection
    Projection
    Update
    Join
    +Aggregations

**Special:**

    View
    Assign


### 2. Immutable Representation (IMR): 

There are benefits and downsides to adding this representation. The idea of the IMR is to force the representation of the dataflow to happen as if all variables are immutable (think Haskell). This alone represents a nudge away from Python's procedural style and towards the style of SQL queries we aim to generate. Admittedly, DBMSs themselves do not have mutability constraints, after all one can freely create and manipulate (temporary) tables, however, due to SQL's declarativeness we usually do not think of mutable dataframes while constructing queries, instead, the focus is on stringing operations together to achieve the result.

```python
Assign(tar = tbl_a_p2d2state_1, src = DBTable(name='customer', conn=conn))
Assign(tar = tbl_b, src = Projection(cols = ['c_custkey', 'c_name', 'c_acctbal'], src = tbl_a_p2d2state_1))
Assign (tar = tbl_c, src = Selection (cols = ['acctbal'], cond = '<800', src = tbl_b))
Assign (tar = tbl_a_p2d2state_2, src = Update (sel = Selection(..), proj = Proj(..), op = '=4' src = tbl_a_p2d2state_1)),
Pull(tar= 'var_b', src = tbl_b),
Action(dependency = 'var_a'),
Pull(tar= 'var_a', src = tbl_a_p2d2state_2),
Action(dependency = 'var_a'),
Ignored(),
Ignored(),
...
```

Now it is much clearer that we are pulling the data-state tbl_a_p2d2state_2 into the Python runtime. tbl_a_p2d2state_2 doesn't change with time, so it is not a question of WHEN to pull var_a, only WHAT query generates it. 

#### Note on Views:

If we decide to support Views we will have to keep the attribute `inPlace = True`. That's important because we do not yet want to forget about the fact that the Assign operation is done in place. In this scenario, var_b (which is tbl_b pulled to the Python runtime.) is actually a selection of tbl_a_p2d2state_2, not tbl_a_p2d2state_1! In the next step, we "resolve" (delete and forget about) views by changing the source of the selection inside the view.

#### Available Nodes (IMR):

Same as PR

### 3. Optimized Representation OpR

The last part of the translation pipeline, OpR resembles an AST tree of a program that was hand-written to utilize the underlying database as much as possible. We still deal with our relational algebra `nodes` but they are nested like SQL queries. First let's try to visualize the operations from the IMR:

```

    DBTable=customer
        |
        a_1 # short for tbl_a_p2d2state_*
        /\
      b    a_2
     /\    |
    c  |   |
       |   |
  ---------------- (Python runtime below 👇)
     var_b var_a 
```

Read this from top to bottom: top is the RDBMS, bottom is the Python runtime, characters are data states, pipes '|' are operations, '/\' represent forks. This visualization makes it clear that the state 'c' (tbl_c from the IMR) ends in neither a Action or a Pull (which means that *c*'s branch can be safely removed. and here is the corresponding OpR, without using Forks:
       

```python
Pull(tar = 'var_a', src=\
    Update (sel = Selection(..), proj = Proj(..), op = '=4' src =\
        DBTable(name='customer', conn=conn)))))
Action(dependency = 'var_a')
Pull(tar = 'var_b' src =\
    Projection(cols = ['c_custkey', 'c_name', 'c_acctbal'], src =\
         DBTable(name='customer', conn=conn)))
Action(dependency = 'var_b'
Ignored()
...
```

Notice that the operations related to *c* are truncated?

We now have a massive single pull line (For clarity I broke the single line with '\')

This example is too short to demonstrate forks. Lets imagine there is an addtional Projection after a_1 and before (b, a_2) named f:

```
    DBTable=customer
        |
        a_1 # short for tbl_a_p2d2state_*
        |
        f
        /\
      b    a_2
     /\    |
    c  |   |
       |   |
  ---------------- (Python runtime below 👇)
     var_b var_a 
```

Now the corresponding OpR would be:

```python
Fork(tar = 'tbl_f', src = Projection (cols = [..], src = DBTable(name='customer', conn=conn)))
Pull(tar = 'var_a', src=\
    Update (sel = Selection(..), proj = Proj(..), op = '=4' src =\
         DBTable(name='tbl_f', conn=conn)))
Action(dependency = 'var_a')
Pull(tar = 'var_b' src =\
    Projection(cols = ['c_custkey', 'c_name', 'c_acctbal'], src = \
        DBTable(name='tbl_f', conn=conn)))
Action(dependency = 'var_b'
Ignored()
...
```

Fork creates a View (or alternatively a TEMP TABLE https://www.postgresql.org/docs/9.3/sql-createtable.html ) which the Pulls for *var_a* and *var_b* use as a final data source.

#### Available Nodes (OpR)

Only the `Fork`, `Pull`, `Action` and `Ignored` are allowed as top-level nodes (compare this to PR and IMR)

#### OpTree

To achieve OpR, we compile the Supported operations of the IR into an Optimization Tree (OpTree). The tree is constructed based on the tar and src attributes of the IMR nodes. The tree is needed for multiple purposes:
1)To spot "loose ends": operations that don't lead to any Actions (consumption from Unsupported operations). After the whole IR is parsed into a tree, If a leaf does not end in an Action, the branch is simply removed - it is redundant.

2) The tree is useful for the Fork optimization, because it shows us when to stop when generating Queries. 

A Query is a LinkedList of operations that always starts with a Pull or a Fork and ends with a Fork or a DBSource

### Nodes explanained

**Pull** - A termination point for our tree (leaf). A Pull is inserted in the AST right before the Action of a specific data-state, E.g. print(df). Pull is translated into a var = pd.read_sql_query() where var is the Pull's target. A Pull is not inserted before subsequent uses of the same variable: If supported mutating operations are executed on the variable, we create a Fork to keep track of the next value state.

**Ignored** - A node that neither consumes nor creates optimizable dataframes. They are left in the AST because they might represent expected side-effects from running the program. Also, any unsupported data transformations after a Pull are of type Ignored.

**Fork** (effect in the database) is translated into:
cur=conn.new_cursor()
cur.execute('CREATE TEMPORARY TABLE t AS (...)')
Translating the fork into a temporary table is not a strict requirement but rather an optimization. That way both branches of the fork can read the temporary data, instead of reexecuting all operations before the fork redundantly.
(PullMutation) If the target variable of a Pull gets manipulated by SupportedOp, we do NOT add Operations after the Pull, instead we insert a Fork right before the pull and continue the operations on the other side of the Fork (a "FunctionalFork") Doing this for UnsupportedOp is simply redundant - would make the ast complex. In a PullMutation, relies on immutable vars/tables (see IMR).


### Supporting Pandas Views

If we have a way to decide if a Pandas operation results in a copy or a view, we have the following implementation options

#### Option 1: SolveView function (manual)

SolveView updates a View's *src* attribute to point to the latest node of the *mother* branch, until the View branch reaches an *Action* ( The mother branch is the branch the View is following ). To illustrate, let's say SolveView receives the following OprTree as input:

```
DBTable(customer) --> a_1 -(inplace operation, t=4)-> a_2 --> | --> var_a
                       \                                      |
                         b (view) --------------------------> | -(t=6)-> var_b
                                                    (python runtime 👉)
```

I am sorry for mixing up the way I visualize trees. The illustration should be read like this: names like a_\* and b are data states after a single operation, arrows (-->) are operations, backslashes (\) are operations that branch out (create a fork), creating either a copy or a view (which is specified in parens). t={number} (time point) denotes at which point the operation is performed, i.e. the inplace operation between a_1 and a_2 is performed before the Pull operation between b and var_b. Using the information, SolveView's output would be (still of type OprTree):

```
DBTable(customer) --> a_1 -(inplace operation, t=4)-> a_2 ---> | --> var_a
                                                       \       |
                                                        b  --> | -(t=6)-> var_b
                                                             (python runtime 👉)
```

The Views are now solved, b is no longer called a view in the tree, because this information is redundant, it does not matter whether b is a view or a copy anymore, since there are no more inplace operations after a_2. The SolveView function is performed after the OpRtree is generated but BEFORE the OpR is generated, This means that no *View* nodes should be present in the OpR, since they should have been solved at this point. Also note that not RDBMS VIEWs were used for option 1.

#### Option 2: RDBMS Views (automatic)

We can avoid SolveView altogether by matching Panda's view with the RDBMS's `CREATE TEMP TABLE`. That way we simulate the existance of the original (mother) pandas dataframe inside the database. All mutations to the original (mother) dataframe are translated to the temporary table and thus we don't need to update the vuews anymore. The disadvantages:

1. Performance?
2. We can't create IMR (Immutable Representation) because we now depend on mutability. 

Question, can replace `CREATE TEMP TABLE` with `CREATE VIEW`? This would require RDBMS VIEWs to support the UPDATE operation, do they support it?

### Fork reduction

Nested Forks can result in high bandwidth consumption. For n forks we end up (assuming no loose ends) with n+1 terminations, in other words, n+1 Pulls. We can have a bandwidth saving mode where we don't pushdown queries if the result is large. As a result, generally, aggregations will still be pushed-down, but where some joins, selections and projections won't be.

### TODO:

How does grizzly handle views?

Can you UPDATE views?

How fast is the creation of a temporary database? Does the DBMS always make a real copy of the data, or does it use lazy evaluation?