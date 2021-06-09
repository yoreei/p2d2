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

import astroid

from pandas._typing import FrameOrSeries
import pandas

pandas_objects = {FrameOrSeries, pandas.DataFrame, pandas.Series}


def pandas_infer(callnode, context=None):
    # Do some transformation here
    return iter((FrameOrSeries,))


def pandas_call_predicate(node):
    if node.root().name not in ("", "__main__"):
        return False

    # print(node.root())
    try:
        obj_type = next(node.func.expr.infer())
    except AttributeError:
        print(f"AttributeError {node.repr_tree()}")
        return False

    # print(obj_type)
    if obj_type in pandas_objects:
        print(node)
        return True
    else:
        print(f"Not pandas object {node.repr_tree()}")
        return False


def pandas_slice_predicate(node):
    obj_type = next(node.value.infer())
    print(obj_type)
    if obj_type in pandas_objects:
        return True
    else:
        return False


astroid.MANAGER.register_transform(
    astroid.nodes.Call,
    astroid.inference_tip(pandas_infer, raise_on_overwrite=True),
    pandas_call_predicate,
)

# astroid.MANAGER.register_transform(
#     astroid.nodes.Subscript,
#     astroid.inference_tip(pandas_infer, raise_on_overwrite=True),
#     pandas_slice_predicate,
# )

parsed = astroid.parse(code)
