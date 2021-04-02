#!/usr/bin/env python3
from pathlib import Path
from io import StringIO
import pandas as pd
import os
import re
import json

INCR=10000 #bytes
listbase = Path('.') # internal HDD
STATEFILE=listbase / 'dldatasets-state.txt'
DATASETSFILE=listbase / 'dldatasets.csv'
KERNELSFILE=listbase / 'dldatasets-kernels.csv'
def get_state():
    if STATEFILE.exists():
        with open(STATEFILE, 'r') as handle:
            state=json.load(handle)
            data=pd.DataFrame(state['data'])
            return data, state['min_size'], state['max_size']
    else:
        return pd.DataFrame(), 0, INCR

def save_state(data, min_size, max_size):
    state={'data':data.to_dict, 'min_size':min_size,'max_size':max_size}
    with open(STATEFILE, 'w') as handle:
        return json.dump(state, handle)
    
            

#def output2df(output:list):
#    dflist=[]
#    for string in output:
#        dflist+=[pd.read_csv(StringIO(string))]
#    df = pd.concat(dflist)
#    return df
def dl_page(cmd, page_no):
    output = os.popen(cmd+f' -p {page_no}').read()
    print(output)
    if re.fullmatch('No \w+ found', output.strip()):
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

def dl_datasets(cmd='kaggle datasets list -v --file-type csv'):
    data, min_size, max_size=get_state()
    while True:
        minpar=f' --min-size {min_size}'
        maxpar=f' --max-size {max_size}'
        if not dl_page(cmd+minpar+maxpar, 500).empty:
            print(f'list too big for {minpar} {maxpar}')
            max_size=(min_size+max_size)/2
            continue
        elif dl_page(cmd+minpar+maxpar, 1).empty:
            if dl_page(cmd+minpar, 1).empty:
                print('all datasets downloaded')
                return data
            else:
                print(f'no results for {minpar} {maxpar}')
                min_size=max_size
                max_size+=INCR
                continue
        else:
            data=data.append(dl_allpages(cmd+minpar+maxpar))
            min_size=max_size
            max_size+=INCR
            save_state(data, min_size, max_size)
            continue

def get_datasets():
    print(f'{DATASETSFILE.exists()=}')
    if DATASETSFILE.exists():
        return pd.read_csv(DATASETSFILE)
    else:
        return dl_datasets()

def dl_kernels(datasets, kerns=100):
    """kerns:max=100"""
    kernels = pd.DataFrame()
    for idx, dataset in enumerate(datasets.ref):
        df=dl_allpages(f'kaggle kernels list -v --page-size {kerns} --dataset {dataset} --language python')
        df['dataset_ref'] = dataset
        kernels=kernels.append(df)
    return kernels


if __name__=='__main__':
    datasets:DataFrame=get_datasets()
    datasets.to_csv(DATASETSFILE, index=False)
    kernels:DataFrame=dl_kernels(datasets)
    kernels.to_csv(KERNELSFILE, index=False)

