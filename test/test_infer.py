import unittest
import astroid
from p2d2.optimizer import inference


class TestInfer(unittest.TestCase):
    def setUp(self):
        inference()

    def typeEqual(self, node, checkType:str):
        inferred = node.inferred()[0] 
        inferred_str = inferred.pytype()
        return self.assertEqual(inferred_str, checkType)

    def test_oop(self):
        code = """
        import pandas as pd  # 0
        # some comment
        d = {'col1': [1, 2], 'col2': [3, 4]} #  1
        df0 = pd.DataFrame(data=d) #  2
        df1 = df0.head(1)  # 3
        app = df0.append(df0)  # 4
        chained = df0.append(df0).head(2).tail(1)  # 5
        chained # 6  Expr(value=Name(..),..)
        """
        parsed = astroid.parse(code)
        checkNode = parsed.body[6].value
        self.typeEqual(checkNode, "pandas.DataFrame")

    def test_proj(self):
        code = """
        import pandas as pd  # 0
        # some comment
        uselesslist = [] # 1
        d = {'col1': [1, 2], 'col2': [3, 4]} #  2
        df0 = pd.DataFrame(data=d) #  3
        proj = df0['col1']  # 4
        proj # 5
        """
        parsed = astroid.parse(code)
        checkNode = parsed.body[5].value
        self.typeEqual(checkNode, "pandas.DataFrame")


    def test_mask(self):
        code = """
        import pandas as pd  # 0
        # some comment
        uselesslist = [] # 1
        d = {'col1': [1, 2], 'col2': [3, 4]} #  2
        df0 = pd.DataFrame(data=d) #  3
        mask = df0['col1']<=1  # 4
        mask #  5
        """
        parsed = astroid.parse(code)
        checkNode = parsed.body[5].value
        self.typeEqual(checkNode, "pandas.DataFrame")

    def test_getitem_mask(self):
        code = """
        import pandas as pd  # 0
        # some comment
        uselesslist = [] # 1
        d = {'col1': [1, 2], 'col2': [3, 4]} #  2
        df0 = pd.DataFrame(data=d) #  3
        mask = df0.__getitem__('col1')<=1  # 4
        mask #  5
        """
        parsed = astroid.parse(code)
        checkNode = parsed.body[5].value
        self.typeEqual(checkNode, "pandas.DataFrame")

    def test_getitem_proj(self):
        code = """
        import pandas as pd  # 0
        # some comment
        d = {'col1': [1, 2], 'col2': [3, 4]}  # 1
        df0 = pd.DataFrame(data=d)  # 2
        proj = df0.__getitem__('col1')  # 3
        proj  # 4 
        """
        parsed = astroid.parse(code)
        checkNode = parsed.body[4].value
        self.typeEqual(checkNode, "pandas.DataFrame")

    # commented out because redundant

    # def test_sel(self):
    #     code = """
    #     import pandas as pd  # 0
    #     # some comment
    #     uselesslist = [] # 1
    #     d = {'col1': [1, 2], 'col2': [3, 4]} #  2
    #     df0 = pd.DataFrame(data=d) #  3
    #     sel = df0[df0['col1']<=1]  # 4
    #     sel #  5
    #     """
    #     parsed = astroid.parse(code)
    #     checkNode = parsed.body[5].value
    #     self.typeEqual(checkNode, "pandas.DataFrame")

    # def test_getitem_sel(self):
    #     code = """
    #     import pandas as pd  # 0
    #     # some comment
    #     d = {'col1': [1, 2], 'col2': [3, 4]}  # 1
    #     df0 = pd.DataFrame(data=d)  # 2
    #     sel = df0.__getitem__(df0.__getitem__('col1')<=1)  # 3
    #     sel # 4
    #     """
    #     parsed = astroid.parse(code)
    #     checkNode = parsed.body[4].value
    #     breakpoint()
    #     self.typeEqual(checkNode, "pandas.DataFrame")

    def test_getattr_head(self):
        code = """
        import pandas as pd  # 0
        # some comment
        uselesslist = [] # 1
        d = {'col1': [1, 2], 'col2': [3, 4]} #  2
        df0 = pd.DataFrame(data=d) #  3
        df1 = getattr(df0, "head")(1)  # 4
        df1  # 5
        """
        parsed = astroid.parse(code)
        checkNode = parsed.body[5].value
        self.typeEqual(checkNode, "pandas.DataFrame")

    def test_getattr_append(self):
        code = """
        import pandas as pd  # 0
        # some comment
        uselesslist = [] # 1
        d = {'col1': [1, 2], 'col2': [3, 4]} #  2
        df0 = pd.DataFrame(data=d) #  3
        df1 = getattr(df0, "head")(1)  # 4
        app = getattr(df0, "append")(df0)  # 5
        app  # 6 
        """
        parsed = astroid.parse(code)
        checkNode = parsed.body[6].value
        self.typeEqual(checkNode, "pandas.DataFrame")

    def test_getattr_nested(self):
        code = """
        import pandas as pd  # 0
        # some comment
        d = {'col1': [1, 2], 'col2': [3, 4]} #  1
        app = getattr(  # 2
                getattr(
                    pd.DataFrame(data=d), # .value.func.args[0].func.args[0]
                    "head")(1
                    ),  #  value.func.args[0].func
                 "append")(
                 pd.DataFrame(data=d) # .value.args[0]
            ) # .value 
        app  # 3 
        """
        parsed = astroid.parse(code)

        # append
        checkNode = parsed.body[2].value
        self.typeEqual(checkNode, "pandas.DataFrame")

        # pd.DataFrame
        checkNode = parsed.body[2].value.args[0]
        self.typeEqual(checkNode, "pandas.DataFrame")
        
        # head
        checkNode = parsed.body[2].value.func.args[0]
        self.typeEqual(checkNode, "pandas.DataFrame")

        # pd.DataFrame
        checkNode = parsed.body[2].value.func.args[0].func.args[0]
        self.typeEqual(checkNode, "pandas.DataFrame")

#    def test_generic(self):
#        code = """
#        import pandas as pd  # 0
#        # some comment
#        uselesslist = [] # 1
#        d = {'col1': [1, 2], 'col2': [3, 4]} #  2
#        df0 = pd.DataFrame(data=d) #  3
#        df1 = df0.head(1)  # 4
#        app = df0.append(df0)  # 5
#        sel = df0[df0['col1']<=1]  # 6
#        proj = df0['col1']  # 7
#        df2 = sel.append(df0)  # 8
#        complex = df0.append(df0).head(2).tail(1)  # 9
#        pylist = [1,2,3,4,5,6,7,8,9]  # 10
#        pylist_slice = pylist[0:3]  # 11
#        pylist_app = pylist.append(10)  # 12
#        """
#        parsed = astroid.parse(code)
#        checkNode = parsed.body[5]
#        self.typeEqual(checkNode, "DataFrame")

