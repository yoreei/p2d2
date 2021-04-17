#!/usr/bin/env python
import pandas as pd
import numpy as np
import IPython

df = pd.DataFrame(np.random.randint(0, 12, size=(12, 4)), columns=list("ABCD"))
na = np.random.randint(0, 12, size=(12, 4))

IPython.embed()
exit()
