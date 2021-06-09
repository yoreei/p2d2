#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import os

listbase = Path(".")  # internal HDD
database = Path("F:/bachelor/bigsample")  # external HDD
KERNELSFILE = listbase / "dlsampldatasets-kernels.csv"
assert KERNELSFILE.exists()

kernels = pd.read_csv(KERNELSFILE, index_col=False)
for ds in kernels["dataset_ref"].unique():
    ds_dir = database / ds / "data"
    print(f"downloading dataset {ds}")
    retcode = os.system(f"kaggle datasets download {ds} -p {ds_dir} ")
    if retcode != 0:
        print("skipping {ds} {retcode=}")
        continue
    for kernel in kernels[kernels["dataset_ref"] == ds]["ref"]:
        kernel_dir = database / ds / "kernels" / kernel
        print(f"downloading kernel {kernel}")
        retcode = os.system(f"kaggle kernels pull {kernel} -p {kernel_dir}")


# datasets=pd.read_csv(DATASETSFILE, index_col=False)['ref']
# for dataset in datasets:
#    folder = database / competition / 'data'
#    #folder.mkdir(parents=True, exist_ok=True)
#    #print(f'crawl-kaggle: Downloading {competition}')
#    retcode = os.system(f'kaggle datasets download -p {folder} {dataset}')
#    print(f'{retcode=}')
#
# kernels=pd.read_csv(base / 'kernels.csv', index_col=False)
# for kernel, competition in zip(kernels.ref, kernels.competition_ref):
#    folder = database / competition / 'kernels' / kernel
#    folder.mkdir(parents=True, exist_ok=True)
#    os.system(f'kaggle kernels pull {kernel} -p {folder}')
