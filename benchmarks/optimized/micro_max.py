#!/bin/env python3
import pandas as pd
import numpy as np
import psycopg2


def action(name):
    return None


conn = psycopg2.connect(CONNSTR)
gmaxi = pd.read_sql_query("SELECT MAX(l_orderkey), l_linenumber FROM lineitem GROUP BY l_linenumber", conn)


action(gmaxi)
