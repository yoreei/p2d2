#!/usr/bin/env python3
from pathlib import Path
from io import StringIO
import pandas as pd
import numpy as np
import os



comp_file='comp-tabular.csv'
comp_cmd='kaggle competitions list -p {} -v'
base = Path('G:/')

if not (base / comp_file).exists():
    print(f'{comp_file} missing, downloading list...')
    data = []
    page_no, output = 1, ""
    while output.strip() != 'No competitions found':
        output = os.popen(comp_cmd.format(page_no)).read()
        data.append(pd.read_csv(StringIO(output)))
        page_no += 1

    competitions = pd.concat(data)
    competitions.to_csv(base / comp_file, index=False)
else:
    print(f'{comp_file}found')
    competitions = pd.read_csv(base / comp_file)
    print(list(competitions), competitions.shape)
    print(competitions)

# print("***", os.popen(f'kaggle kernels list --page-size 100 --competition titanic --language python -p 10000 -v').read().strip(), "***")


if not (base / 'kernels.csv').exists():
    print('kernels.csv not found. Downloading list')
    data = []
    for idx, competition in enumerate(competitions.ref):
        page_no, output = 1, ""
        while output.strip() != 'No kernels found':
            # kaggle kernels pull -k [KERNEL] -p /path/to/download -m
            output = os.popen(f'kaggle kernels list --page-size 100 --competition {competition} --language python -p {page_no} -v').read()
            df = pd.read_csv(StringIO(output))
            df['competition_ref'] = competition
            data.append(df)
            page_no += 1
            print("Competition", competition, f"done. {idx+1}/{competitions.shape[0]}")

    kernels = pd.concat(data)
    kernels.to_csv(base / 'kernels.csv', index=False)

else:
    print('kernels.csv found')
    kernels = pd.read_csv(base / 'kernels.csv')
    print(list(kernels), kernels.shape)

print(kernels)

