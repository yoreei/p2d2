import time
import sqlalchemy
start_clock = time.perf_counter()
query="""
select
	s_acctbal,
	s_name,
	n_name,
	p_partkey,
	p_mfgr,
	s_address,
	s_phone,
	s_comment
from
	part,
	supplier,
	partsupp,
	nation,
	region
where
	p_partkey = ps_partkey
	and s_suppkey = ps_suppkey
	and p_size = 38
	and p_type like '%TIN'
	and s_nationkey = n_nationkey
	and n_regionkey = r_regionkey
	and r_name = 'MIDDLE EAST'
	and ps_supplycost = (
		select
			min(ps_supplycost)
		from
			partsupp,
			supplier,
			nation,
			region
		where
			p_partkey = ps_partkey
			and s_suppkey = ps_suppkey
			and s_nationkey = n_nationkey
			and n_regionkey = r_regionkey
			and r_name = 'MIDDLE EAST'
	)
order by
	s_acctbal desc,
	n_name,
	s_name,
	p_partkey
LIMIT 100;
"""
import pandas as pd
import numpy as np

query = sqlalchemy.text(query)
result = pd.read_sql(query, con=CONNSTR)
#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock
SHARED_WALL_TIME.value = time.perf_counter() - start_clock
