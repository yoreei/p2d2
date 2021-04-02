#!/usr/bin/env python3
from pathlib import Path
from io import StringIO
import pandas as pd
import numpy as np
import os
import re
import json

base = Path('G:/')
INCR=10000 #bytes
STATEFILE=base / 'dldatasetsstate.txt'
def get_state():
    if STATEFILE.exists():
        with open(STATEFILE, 'r') as handle:
            return json.load(handle)
    else:
        state={}
        state['data']=[]
        state['min_size']=0
        state['max_size']=INCR
        return state

def save_state(state):
    with open(STATEFILE, 'w') as handle:
        return json.dump(state, handle)
    
            

MAX_PAGES=500 # API limit

def output2df(output:list):
    dflist=[]
    for string in output:
        dflist+=[pd.read_csv(StringIO(string))]
    df = pd.concat(dflist)
    return df
def dl_page(cmd, page_no):
    output = os.popen(cmd+f' -p {page_no}').read()
    print(output)
    if re.fullmatch('No \w+ found', output.strip()):
        return None
    else:
        return pd.DataFrame(output)

def dl_allpages(cmd):
    allpages = []
    for page_no in range(1,MAX_PAGES):
        page=dl_page(cmd, page_no)
        if page==None:
            return allpages
        else:
            allpages.append(page)

    return allpages

def dl_datasets(cmd='kaggle datasets list -v --file-type csv'):
    state=get_state()
    while True:
        min_size=state['min_size']
        max_size=state['max_size']
        minpar=f' --min-size {min_size}'
        maxpar=f' --max-size {max_size}'
        if dl_page(cmd+minpar+maxpar, MAX_PAGES):
            print(f'list too big for {minpar} {maxpar}')
            max_size=(min_size+max_size)/2
            continue
        elif not dl_page(cmd+minpar+maxpar, 1):
            if not dl_page(cmd+minpar, 1):
                print('all datasets downloaded')
                return data
            else:
                print(f'no results for {minpar} {maxpar}')
                min_size=max_size
                max_size+=INCR
                continue
        else:
            state['data']+=dl_allpages(cmd+minpar+maxpar)
            state['min_size']=state['max_size']
            state['max_size']+=INCR
            save_state(state)
            continue

def get_datasets():
    exists=(base / 'datasets.csv').exists()
    print(f'datasets.csv exists?: {exists}')
    if not exists:
        return output2df(dl_datasets())
    else:
        return pd.read_csv(base / 'datasets.csv')

def get_kernels(datasets):
    exists=(base / 'dataset_kernels.csv').exists()
    print(f'datase_kernels.csv exists?: {exists}')
    if not exists:
        return dl_kernels(datasets)
    else:
        return pd.read_csv(base / 'dataset_kernels.csv')

def dl_kernels(datasets):
    kernels = pd.DataFrame()
    for idx, dataset in enumerate(datasets.ref):
        output=dlallpages(f'kaggle kernels list -v --page-size 100 --dataset {dataset} --language python')
        df=output2df(output)
        df['dataset_ref'] = dataset
        kernels=kernels.append(df)
    return kernels


if __name__=='__main__':
    datasets=get_datasets()
    datasets.to_csv(base / 'datasets.csv', index=False)
    kernels=get_kernels(datasets)
    kernels.to_csv(base / 'kernels.csv', index=False)

