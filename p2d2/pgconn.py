#!/usr/bin/env python3

import psycopg2

#import pandas.io.sql as sqlio
#dat = sqlio.read_sql_query(sql, conn)

def get(dbname='tpch'):
    return psycopg2.connect(f"host=localhost dbname={dbname} user=vagrant password=vagrant")
