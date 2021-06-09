import astroid


def _pandas_transform():
    return astroid.parse(
        """
    class DataFrame(dict):
        # def __init__(
        #     self,
        #     data=None,
        #     index = None,
        #     columns = None,
        #     dtype = None,
        #     copy = None,
        # ): pass
        def head(self, num): return self
        def tail(self, num): return self
        def append(self, df2): return self 

        # def __missing__(self, key): pass
        def __getitem__(self, key): return self

    """
    )


astroid.register_module_extender(astroid.MANAGER, "pandas", _pandas_transform)


code = """
import pandas as pd  # 0
# some comment
uselesslist = [] # 1
d = {'col1': [1, 2], 'col2': [3, 4]} #  2
df0 = pd.DataFrame(data=d) #  3
df1 = df0.head(1)  # 4
app = df0.append(df0)  # 5
sel = df0[df0['col1']<=1]  # 6
proj = df0['col1']  # 7
df2 = sel.append(df0)  # 8
complex = df0.append(df0).head(2).tail(1)  # 9
pylist = [1,2,3,4,5,6,7,8,9]  # 10
pylist_slice = pylist[0:3]  # 11
pylist_app = pylist.append(10)  # 12
"""
