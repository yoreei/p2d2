import astroid

no_returns = []
with_returns = []


def pandas_infer(node, context=None):
    # Do some transformation here
    return iter((node.returns.name,))


def pandas_call_predicate(node):
    # print(node.root())
    if node.returns:
        # print(node.name, node.root().name, sep='; ')
        with_returns.append(node.name + "; " + node.root().name)
        return True
    else:
        no_returns.append(node.name + "; " + node.root().name)
        return False


astroid.MANAGER.register_transform(
    astroid.nodes.FunctionDef,
    astroid.inference_tip(pandas_infer, raise_on_overwrite=True),
    pandas_call_predicate,
)

code = """
import pandas as pd  # 0
from pandas.core import generic # 1
import pandas.DataFrame # 2
# some comment
uselesslist = [] # 3
d = {'col1': [1, 2], 'col2': [3, 4]} #  4
df0 = pd.DataFrame(data=d) #  5
df1 = df0.head(1)  # 6
app = df0.append(df0)  # 7
sel = df0[df0['col1']<=1]  # 8
proj = df0['col1']  # 9
df2 = sel.append(df0)  # 10
complex = df0.append(df0).head(2).tail(1)  # 11
pylist = [1,2,3,4,5,6,7,8,9]  # 12
pylist_slice = pylist[0:3]  # 13
pylist_app = pylist.append(10)  # 14
"""
parsed = astroid.parse(code)
body = parsed.body
inf = body[6].value.infer()
next(inf)
