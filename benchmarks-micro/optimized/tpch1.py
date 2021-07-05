import time
start_clock = time.perf_counter()
query = """
select
	l_returnflag,
	l_linestatus,
	sum(l_quantity) as sum_qty,
	sum(l_extendedprice) as sum_base_price,
	sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
	sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
	avg(l_quantity) as avg_qty,
	avg(l_extendedprice) as avg_price,
	avg(l_discount) as avg_disc,
	count(*) as count_order
from
	lineitem
where
	l_shipdate <= date '1998-09-01'
group by
	l_returnflag,
	l_linestatus
order by
	l_returnflag,
	l_linestatus;
"""
import pandas as pd
import numpy as np


result = pd.read_sql_query(query, con=CONNSTR)
#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock
SHARED_WALL_TIME.value = time.perf_counter() - start_clock
print(time.perf_counter() - start_clock)
