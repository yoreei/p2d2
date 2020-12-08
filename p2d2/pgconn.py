#!/usr/bin/env python3

import psycopg2

#import pandas.io.sql as sqlio
#dat = sqlio.read_sql_query(sql, conn)

def get():
    return psycopg2.connect("host=localhost dbname=tpch user=vagrant password=vagrant")
