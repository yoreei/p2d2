
import ast
from itertools import *
from collections import Counter
import pandas as pd
from pathlib import Path
import operator as op
import typing

def in_all_files(rootdir: str) -> pd.DataFrame:
    report_dict = {'dataset':[], 'size':[]}
    all_zips = list(Path(rootdir).glob("**/*.zip"))
    all_zips_count = len(all_zips)
    for idx, dataset in enumerate(all_zips):
        report_dict['dataset'].append(str(dataset))
        report_dict['size'].append(dataset.stat().st_size)
        print(f"{idx} / {all_zips_count}")
        print(report_dict['dataset'][-1])
        print(report_dict['size'][-1])

    
    return pd.DataFrame.from_dict(report_dict)

if __name__ == "__main__":

    try:
        report = in_all_files("G:/bachelor/bigsample")
        report.reset_index(inplace=True)
        report.to_feather("dataset_sizes.feather", compression="uncompressed")
    except Exception as e:
        raise e
    finally:
        import sys
        sys.path.append("../p2d2/benchmarker")
        import finished_hook
        finished_hook.fire()
