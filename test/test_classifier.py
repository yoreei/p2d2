import unittest
import astroid
from p2d2.IRBuilder.classifier import dictify
from p2d2.infer.inference import inference


class TestDictify(unittest.TestCase):
    """In order to isolate the tests, the code snippets are provided in an SSA+ANF compatible form + some desugarizations
    """
    def setUp(self):
        inference()

    def test_read_sql_table(self):
        code = """import pandas
import psycopg2
c = psycopg2.connect(f"host=localhost dbname=tpch10 user=p2d2 password=p2d2")
t = pandas.read_sql_table(table_name = "table", con = c)
"""
        parsed = astroid.parse(code)
        testing_node = parsed.body[3].value
        #breakpoint()
        state={
            "c":{"type":"psycopg2.extensions.connection"}
            }
        dictified = dictify(testing_node, state)
        expected = {
            "attrname": "read_sql_table",
            "self_type": "pandas",
            "kwargs_values": {"table_name": "table", "con" : None}, 
            #"kwargs_types": {"table_name": "str", "con" : "psycopg2.extensions.connection"},
            "kwargs_types": {"table_name": "builtins.str", "con" : "psycopg2.extensions.connection"},
            "kwargs_varnames": {"table_name": "", "con" : "c"}
            }
        self.assertEqual(dictified, expected)
        
    def test_getitem_dataframe(self):
        code = """import pandas
t = pandas.read_sql_table("table", object())
m = t.__getitem__(key = "col") > 5
p = t.__getitem__(key = m)
"""
        parsed = astroid.parse(code)
        testing_node = parsed.body[3].value
        # breakpoint()
        dictified = dictify(testing_node, state={})
        expected = {
            "attrname":"__getitem__",
            "self_type": "pandas.DataFrame",
            "kwargs_values":{"key": None},
            "kwargs_types":{"key":"pandas.DataFrame"},
            "kwargs_varnames": {"key": "m"}
        }
        self.assertEqual(dictified, expected)

    def test_getitem_str(self):
        code = """import pandas
t = pandas.read_sql_table("table", object())
p = t.__getitem__(key = "col") #2
"""
        parsed = astroid.parse(code)
        testing_node = parsed.body[2].value
        dictified = dictify(testing_node, state={})
        expected = {
            "attrname":"__getitem__",
            "self_type": "pandas.DataFrame",
            "kwargs_values":{"key": "col"},
            #"kwargs_types":{"key":"str"},
            "kwargs_types":{"key":"builtins.str"},
            "kwargs_varnames": {"key": ""}
        }
        self.assertEqual(dictified, expected)

    def test_getitem_list(self):
        code = """import pandas
t = pandas.read_sql_table("table", object())
p = t.__getitem__(key = ["col"])
"""
        parsed = astroid.parse(code)
        testing_node = parsed.body[2].value
        #breakpoint()
        dictified = dictify(testing_node, state={})
        expected = {
            "attrname":"__getitem__",
            "self_type": "pandas.DataFrame",
            "kwargs_values":{"key": ["col"]},
            "kwargs_types":{"key":"builtins.list"},
            #"kwargs_types":{"key":"list"},
            "kwargs_varnames": {"key": ""}
        }
        self.assertEqual(dictified, expected)

    def test_groupby(self):
        code = """import pandas
t = pandas.read_sql_table("table", object())
g = t.groupby(by="col")
"""
        parsed = astroid.parse(code)
        testing_node = parsed.body[2].value
        dictified = dictify(testing_node, state={})
        expected = {
            "attrname":"groupby",
            "self_type": "pandas.DataFrame",
            "kwargs_values":{"by": "col"},
            "kwargs_types":{"by":"builtins.str"},
            #"kwargs_types":{"by":"str"},
            "kwargs_varnames": {"by": ""}
        }
        self.assertEqual(dictified, expected)

    def test_groupby_max(self):
        code = """import pandas
t = pandas.read_sql_table("table", object())
g = t.groupby(by="col")
m = g.max()
"""
        parsed = astroid.parse(code)
        testing_node = parsed.body[3].value
        dictified = dictify(testing_node, state={})
        expected = {
            "attrname":"max",
            "self_type":"pandas.GroupBy",
            "kwargs_values":{},
            "kwargs_types":{},
            "kwargs_varnames": {}
        }
        self.assertEqual(dictified, expected)

