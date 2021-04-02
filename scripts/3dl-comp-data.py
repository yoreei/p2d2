#!/usr/bin/env python3
from pathlib import Path
from io import StringIO
import pandas as pd
import os

base = Path('G:/kaggle')

competitions_series=pd.read_csv('competitions.csv', index_col=False)['ref']
competitions=list(competitions_series)

for competition in competitions:
    folder = base / competition / 'data'
    folder.mkdir(parents=True, exist_ok=True)
    print(f'crawl-kaggle: Downloading {competition}')
    output = os.system(f'kaggle competitions download -p {folder} {competition}')
    if output == 0: #check if correct
        with open("done", "a") as donefile:
            donefile.write(competition+'\n')
    
        
    print(f'crawl-kaggle: Kaggle command output: {output}')

# the kaggle command will skip downloading
# if local copy is found
#
#def readconfig(name):
#    if Path(name).exists():
#        return pd.read_csv(name, header = None, index_col=False, squeeze=True)
#
#    return pd.Series([])
#doneset = set(readconfig('done'))
#competitions_set = set(kernels.competition_ref)
#competitions = competitions_set - doneset
