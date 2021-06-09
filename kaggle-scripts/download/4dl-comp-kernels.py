#!/usr/bin/env python3
from pathlib import Path
from io import StringIO
import pandas as pd
import numpy as np
import os


base = Path("G:/")

if not (base / "kernels.csv").exists():
    print("kernels.csv not found")
    exit()

#

kernels = pd.read_csv(base / "kernels.csv", index_col=False)
for kernel, competition in zip(kernels.ref, kernels.competition_ref):
    folder = base / "kernels" / competition
    folder.mkdir(parents=True, exist_ok=True)
    os.system(f"kaggle kernels pull {kernel} -p {folder}")

# variance of grammar
