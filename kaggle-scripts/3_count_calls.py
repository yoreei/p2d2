import ast
from itertools import *
from collections import Counter
from pprint import pprint
import pandas as pd
from pathlib import Path
import operator as op
import typing


def ast_find(root, node_type) -> typing.Generator:
    return filter(lambda x: isinstance(x, node_type), ast.walk(root))


def count_functions(parsed) -> pd.DataFrame:
    calls = ast_find(parsed, ast.Call)
    # uncomment below to ignore the tail of long fluid interface lines
    # calls = filter(lambda x: isinstance(x.func, ast.Name), calls)
    counter = Counter()
    for call in calls:
        # e.g. print()
        if isinstance(call.func, ast.Name):
            func_name = call.func.id
        # e.g. pd.DataFrame()
        if isinstance(call.func, ast.Attribute):
            func_name = call.func.attr # attrname in astroid parlance

        counter[func_name] += 1
        
    return pd.DataFrame(counter.most_common(), columns=["Function", "Counter"])


def files_read(rootdir: str, glob: str = "**/*") -> typing.Generator:
    for f_path in Path(rootdir).glob(glob):
        print(f_path)
        with open(f_path, encoding='utf-8') as f_obj:
            yield (f_path, f_obj.read())


def in_all_files(rootdir: str) -> pd.DataFrame:
    report = pd.DataFrame()
    kernels_text: typing.Generator = files_read(rootdir, "**/*.py")
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


if __name__ == "__main__":
    """
    TODO: include library in case the call is: library.function
    """

    report = in_all_files("G:/bachelor/bigsample")
    report.to_csv("func_report7Jul.csv", index=False)
    print("---counting complete---")

    # import doctest
    # doctest.testmod()
