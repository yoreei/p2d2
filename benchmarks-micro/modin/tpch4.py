import time
start_clock = time.perf_counter()
import modin.pandas as pd
import numpy as np

### DEBUG:
# CONNSTR='postgresql://root:root@localhost/tpch1'
# from types import SimpleNamespace
# SHARED_DB_TIME=SimpleNamespace()
### END DEBUG

def udf_disc_price(extended, discount):
    import numpy as np
	return np.multiply(extended, np.subtract(1, discount))

def udf_charge(extended, discount, tax):
    import numpy as np
	return np.multiply(extended, np.multiply(np.subtract(1, discount), np.add(1, tax)))

    
orders = pd.read_sql("SELECT * FROM orders", parse_dates=['o_orderdate'], con=CONNSTR)

lineitem = pd.read_sql("SELECT * FROM lineitem", parse_dates = ['l_shipdate', 'l_commitdate', 'l_receiptdate'], con=CONNSTR)

orders = orders.astype({'o_orderstatus' : 'category', 'o_orderpriority' : 'category'})
lineitem = lineitem.astype({'l_returnflag': 'category', 'l_linestatus': 'category'})

#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock


l = lineitem[["l_orderkey", "l_commitdate"]][lineitem.l_commitdate < lineitem.l_receiptdate][["l_orderkey"]]
o = orders[["o_orderkey", "o_orderpriority", "o_orderdate"]][(orders.o_orderdate >= "1997-07-01") & (orders.o_orderdate < "1997-10-01")][["o_orderkey", "o_orderpriority"]]
lo = l.merge(o, left_on="l_orderkey", right_on="o_orderkey").drop_duplicates()[["o_orderpriority"]]
result = lo.groupby("o_orderpriority").size().reset_index(name='counts').sort_values('o_orderpriority')

SHARED_WALL_TIME.value = time.perf_counter() - start_clock
