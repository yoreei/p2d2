import pandas
from pathlib import Path
from itertools import *
import operator as op


def write(df: pandas.DataFrame, path: str):
    suffix = Path(path).suffix  # ex. '.csv'
    stem = Path(path).stem
    numbers = map(str, count(1))
    versioned_stems = map(op.add, repeat(stem), numbers)
    versioned_names = map(op.add, versioned_stems, repeat(suffix))
    free_names = filter(lambda x: not Path(x).exists(), versioned_names)
    df.to_csv(next(free_names), index=False)
