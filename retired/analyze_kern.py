# type(red[1])==ImportNode
# red[1].value[0].value[0].value == 'pandas'

# type(red[1])==FromImportNode
# red2[0].value[0].value=='pandas'


# GetitemNode a[]
# DotNode a.hjkjj
from redbaron import RedBaron
import redbaron
from itertools import *


def rename(red, orig, new):
    nodes: list = red("name", value=orig)
    for node in nodes:
        node.value = new


def remove_importas(red):
    """
    >>> with open('barontest.py','r') as f:
    ...  red=RedBaron(f.read())
    >>> remove_importas(red)
    >>> 'pd' in red.dumps()
    False
    """
    nodes: list = red("DottedAsNameNode", target=lambda x: x != "")
    for node in nodes:
        tar = node.target  # pd
        src = node.value[0].value  # pandas
        rename(red, orig=tar, new=src)
        node.target = ""


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


def count_functions(red):
    calls = red("call")
    counter = Counter(map(lambda x: x.parent.value[x.index_on_parent - 1].value, calls))
    return pd.DataFrame(counter.most_common(), columns=["Function", "Counter"])


from pathlib import Path


def in_all_files(rootdir: Path):
    report = pd.DataFrame()
    for kernel in rootdir.glob("**/*-utf8.py"):
        print(kernel)
        with open(kernel) as f:
            try:
                red = RedBaron(f.read())
            except UnicodeDecodeError:
                print(f"skipping {kernel=} due to UnicodeDecodeError", file=sys.stderr)
                continue
            except redbaron.baron.parser.ParsingError:
                print(f"skipping {kernel=} due to ParsingError", file=sys.stderr)
                continue
        count = count_functions(red)
        count["Kernel"] = kernel
        report = report.append(count)
    return report


if __name__ == "__main__":
    import sys

    rootdir = Path(sys.argv[1])
    report = in_all_files(rootdir)
    report.to_csv("func_report.csv", index=False)

    # import doctest
    # doctest.testmod()
