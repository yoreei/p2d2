import unittest
import p2d2.optimizer as optimizer
import pandas

def assertFrameEqual(df1, df2, **kwds ):
    """ Assert that two dataframes are equal, ignoring ordering of columns"""
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.sort_index(axis=1), df2.sort_index(axis=1), check_names=True, **kwds )

class TestAPI (unittest.TestCase):
    def setUp(self):
        inference()

    def test_join(self):
        code="""
import pandas as pd
import psycopg2
conn = psycopg2.connect(f"host=localhost dbname=tpch1 user=p2d2 password=p2d2")

df1 = pd.read_sql_query("SELECT * FROM customer", conn)
df2 = pd.read_sql_query("SELECT * FROM orders", conn)

joined = df1.merge(
    right=df2,
    how="inner",
    left_on="c_custkey",
    right_on="o_custkey",
    suffixes=("_x", "_y"),
)
# joined.sort_values(by='o_orderkey')
joined.to_csv('logs/{}.csv', index=False)
"""
        pandas_code = code.format('pandas_join')
        p2d2_code = code.format('p2d2_join')
        p2d2_optimized = optimizer.optimize(p2d2_code, "host=localhost dbname=tpch1 user=p2d2 password=p2d2")
        
        exec(compile(p2d2_optimized, filename='<string>', mode='exec'))
        exec(compile(pandas_code, filename='<string>', mode='exec'))
        
        df1=pandas.read_csv('logs/pandas_join.csv')
        df2=pandas.read_csv('logs/p2d2_join.csv')

        self.assertTrue(assertFrameEqual(df1,df2))
