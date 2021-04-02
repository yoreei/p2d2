# After this run 3dldatasets-data-kerns.py

from pathlib import Path
from io import StringIO
import pandas as pd
import os
import re
listbase = Path('.') # internal HDD, 3rd step will use external HDD
DATASETSFILE=listbase / 'dlsampldatasets.csv' # not actually used by 3rd step
KERNELSFILE=listbase / 'dlsampldatasets-kernels.csv'

def dl_page(cmd, page_no):
    output = os.popen(cmd+f' -p {page_no}').read()
    print(f'{locals()=}')
    if re.fullmatch('(No \w+ found)|()', output.strip()):
        return pd.DataFrame() # empty means false
    else:
        return pd.read_csv(StringIO(output))

def dl_allpages(cmd, max_pages=500):
    """max_pages:max=500"""
    allpages = pd.DataFrame()
    for page_no in range(1,max_pages):
        page=dl_page(cmd, page_no)
        if page.empty:
            return allpages
        else:
            allpages=allpages.append(page)

    return allpages

def dl_kernels(datasets, kerns=100):
    """kerns:max=100"""
    kernels = pd.DataFrame()
    for idx, dataset in enumerate(datasets.ref):
        df=dl_allpages(f'kaggle kernels list -v --page-size {kerns} --dataset {dataset} --language python')
        df['dataset_ref'] = dataset
        kernels=kernels.append(df)
    return kernels

if __name__=='__main__':
    datasets=dl_allpages('kaggle datasets list -v --file-type csv')
    datasets.to_csv(DATASETSFILE, index=False)
    kernels=dl_kernels(datasets)
    kernels.to_csv(KERNELSFILE, index=False)


