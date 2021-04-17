# type(red[1])==ImportNode
# red[1].value[0].value[0].value == 'pandas'

# type(red[1])==FromImportNode
# red2[0].value[0].value=='pandas'


# GetitemNode a[]
# DotNode a.hjkjj
import ast
from itertools import *


def ast_find(root, node_type):
    return filter(lambda x: isinstance(x, node_type), ast.walk(root))


# def rename(red, orig, new):
#     nodes:list = red('name', value=orig)
#     for node in nodes:
#         node.value=new
#
# def remove_importas(red):
#     """
#     >>> with open('barontest.py','r') as f:
#     ...  red=RedBaron(f.read())
#     >>> remove_importas(red)
#     >>> 'pd' in red.dumps()
#     False
#     """
#     nodes:list = red('DottedAsNameNode', target=lambda x:x!='')
#     for node in nodes:
#         tar=node.target # pd
#         src=node.value[0].value # pandas
#         rename(red, orig=tar, new=src)
#         node.target=''

# def _split_points(identifier):
#    atoms=red('atomtrailers')
#    split_points = iter([])
#    for atom in atoms:
#        identifiers=atom(indentifier)
#        indexes = [i.index_on_parent+1 for i in identifiers]
#        atom_split_points = filter(indexes, lambda x:x<len(atoms))
#        split_endings = chain(atom_split_points, [None])
#        split_points = chain(split_points, (zip(repeat(atom), atom_split_points)))
#
#    return split_points
# def _produce_node(atom, prev_name, start, stop):
#    newname = hash(atom[start, stop])
#    prev_name = '' if prev_name is None else prev_name+'.'
#    newline = RedBaron(f'{newname} = {prevname}__replaceme__')
#
# def split_atomtrailers(red):
#    #atoms = red('atomtrailers')
#    #if atoms == []:
#    #    return
#    split_points=_split_points('call')
#    if split_points == []:
#        return
#
#    prev_split=0
#    prev_name=None
#    for atom, split_point in split_points:
#        if split_point == None:
#            del atom[0:prev_split]
#            prev_split=0
#        prev_name = _produce_node(atom, prev_name, prev_split, split_point)
#        prev_split=split_point


def _split_one_atomtrailers(atomtrailers):
    # atomtrailers.value is DotProxyList
    if len(atomtrailers <= 2):
        return
    newname = "p2d2" + hash(atomtrailers.value[0:2])
    newnode = RedBaron(f"{newname} = __p2d2replaceme__")
    newnode[0].value = atomtrailers[0:2]
    del atomtrailers[0:2]
    atomtrailers.insert()  # TODO continue
    line = atomtrailers.absolute_bounding_box.top_left.line
    penultimate = atomtrailers.root.at(line)
    penultimate.insert_before(newnode)
    return _split_one_atomtrailers(atomtrailers)


def split_all_atomtrailers(red):
    for atomtrailers in red("atomtrailers"):
        _split_one_atomtrailers(code, atomtrailers)


from collections import Counter
from pprint import pprint
import pandas as pd


def count_functions(parsed):
    calls = ast_find(parsed, ast.Call)
    simple = filter(lambda x: isinstance(x.func, ast.Name), calls)
    counter = Counter(map(lambda x: x.func.id, simple))
    return pd.DataFrame(counter.most_common(), columns=["Function", "Counter"])


from pathlib import Path


def files_read(rootdir: str, glob: str = "**/*"):
    for f_path in Path(rootdir).glob(glob):
        print(f_path)
        with open(f_path) as f_obj:
            yield (f_path, f_obj.read())


def in_all_files(rootdir: str):
    report = pd.DataFrame()
    kernels_text = files_read(rootdir, "**/*.py")
    successful = 0
    for idx, (kernel_path, kernel) in enumerate(kernels_text):
        try:
            parsed = ast.parse(kernel)
        except SyntaxError:
            continue
        successful += 1
        count_df = count_functions(parsed)
        count_df["Kernel"] = kernel_path
        report = report.append(count_df)
    print(f"{idx+1=}, {successful=}")
    return report


import operator as op


def version_save(df: pd.DataFrame, path: str):
    suffix = Path(path).suffix  # ex. '.csv'
    stem = Path(path).stem
    numbers = map(str, count(1))
    versioned_stems = map(op.add, repeat(stem), numbers)
    versioned_names = map(op.add, versioned_stems, repeat(suffix))
    free_names = filter(lambda x: not Path(x).exists(), versioned_names)
    df.to_csv(next(free_names), index=False)


import astroid


def test():
    code2 = """
import pandas as pd
uselesslist = []
d = {'col1': [1, 2], 'col2': [3, 4]}
df0 = pd.DataFrame(data=d)
df1 = df0.head(1)
dfappend = df0.append(df0)
dftail = df0.tail(1)
dfloc = df0.loc[0]
dfadd = df0 + 1
dfadd = df0.add(1)
dfmul = df0*2
dfmul = df0.mul(2)
dfwhere = df0.where(df0 % 3 == 0, -df0)
intmax = df0.max()
sel = df0[df0['col1']<=1]
proj = df0['col1']
"""
    parsed = astroid.parse(code2)
    inf = parsed.body[-1].targets[0].infer()

    return inf
    # next(inf)
    # <Instance of pandas.core.frame.DataFrame at 0x1694640982624>


if __name__ == "__main__":
    """
    %run analyze_kern_ast.py D:\sample1
    """
    import sys

    rootdir = sys.argv[1]
    report = in_all_files(rootdir)
    version_save(report, "func_report.csv")

    # import doctest
    # doctest.testmod()
