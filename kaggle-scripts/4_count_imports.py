#import astroid
import ast
from itertools import *
from collections import Counter
import pandas as pd
from pathlib import Path
import operator as op
import typing


def ast_find(root, node_type) -> typing.Generator:
    return filter(lambda x: isinstance(x, node_type), ast.walk(root))


def count_functions(parsed) -> pd.DataFrame:
    imports = ast_find(parsed, ast.Import)
    # prepare a dict of lists to create a df from
    counter = dict()
    for an_import in imports:
        for alias in an_import.names:
            # name might be "pandas.DataFrame"
            leftmost_name = alias.name.split(".")[0]
            counter[leftmost_name] = [True]

    importFroms = ast_find(parsed, ast.ImportFrom)
    for importFrom in importFroms:
            leftmost_name = importFrom.module.split(".")[0]
            counter[leftmost_name] = [True]
        
    return pd.DataFrame(counter)


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

    try:
        report = in_all_files("G:/bachelor/bigsample")
        report.fillna(False, inplace=True)
        report.reset_index(inplace=True)
        report['Kernel']=report['Kernel'].astype(str)
        report.to_feather("import_report9Jul.feather")
    except Exception as e:
        raise e
    finally:
        import sys
        sys.path.append("../p2d2/benchmarker")
        import finished_hook
        finished_hook.fire()
