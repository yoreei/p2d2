# how to do type inference with rope
from rope.base import libutils
import ropeutils

project = ropeutils.sample_project()
code2 = """import pandas as pd
import scipy
# some comment
uselesslist = []
d = {'col1': [1, 2], 'col2': [3, 4]}
df0 = pd.DataFrame(data=d)
df1 = df0.head(1)
sel = df0[df0['col1']<=1]
proj = df0['col1']
df2 = sel.append(df0)
"""
scope2 = libutils.get_string_scope(project, code2)
scope2["df2"].get_object().get_type().get_name()
# Out: DataFrame
# TODO how to know it's pandas.DataFrame ?
