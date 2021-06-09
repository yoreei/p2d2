# --- imports
import pandas
import pandas as pd
import psycopg2

# --- df creation
a = pd.DataFrame()

# --- func defs
def my_action(hi, **kwargs):
    return hi


d = {}
# --- func calls
func("hi", **d)
a.append(d)
pandas.somefunc(a)

conn = psycopg2.connect(f"host=localhost dbname=tpch user=p2d2 password=p2d2")


def action(name):
    return None


# --- normal proj
a["henlo"]
b = a["henlo"]

# --- normal sel
a[a["henlo"] < 5]

# ----loc proj

b = a.loc[:, ["l_linenumber", "l_orderkey", "l_comment"]]

# ----loc sel

mask = a.loc[:, "l_linenumber"] <= 5
sel = a.loc[mask]

# ---readsql
df1 = pd.read_sql_query("SELECT * FROM orders", conn)
df2 = pd.read_sql_query("SELECT * FROM customer", conn)

# ------join/merge
joined = df1.merge(
    right=df2,
    how="inner",
    left_on="o_custkey",
    right_on="c_custkey",
    suffixes=("_x", "_y"),
)

action(joined)

# ----groupby
gmaxi = df.groupby(["l_partkey"]).max()
action(gmaxi)

# ---mixed
df1 = pd.read_sql_query("SELECT * FROM orders", conn).loc[:, "henlo"]
