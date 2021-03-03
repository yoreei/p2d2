#!/usr/bin/env python3
from pathlib import Path
from io import StringIO
import pandas as pd
import numpy as np
import os



base = Path('.')

if not (base / 'competitions.csv').exists():
    print('competitions.csv missing, downloading list...')
    data = []
    page_no, output = 1, ""
    while output.strip() != 'No competitions found':
        output = os.popen(f'kaggle competitions list -p {page_no} -v').read()
        data.append(pd.read_csv(StringIO(output)))
        page_no += 1

    competitions = pd.concat(data)
    competitions.to_csv(base / 'competitions.csv', index=False)
else:
    print('competitions.csv found')
    competitions = pd.read_csv(base / 'competitions.csv')
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

"""
for kernel, competition in zip(kernels.ref, kernels.competition_ref):
    folder = base / 'kaggle' / competition
    folder.mkdir(parents=True, exist_ok=True)
    os.system(f'kaggle kernels pull {kernel} -p {folder}')
"""

#variance of grammar
