#!/usr/bin/env python3
"""
Produces csv reports from microbenchmarks
"""
import subprocess
import os
from datetime import datetime

import pandas
import psycopg2

from . import log
from . import monitor as mon

logger = log.getLogger(__name__)

C_TIMES = 2 # CONFIG THIS
# default value used for shorter pipelines runs


def shape_traffic(area: str):

    child = subprocess.Popen(["/bin/bash", f"./net/{area}.sh"])
    child.communicate()
    rc = child.returncode
    assert rc == 0
    return rc

# FIX CONNSTR IF NEEDED
# def exec_sql(query):
#     # global CONNSTR we don't change it
#     conn = psycopg2.connect(CONNSTR)
#     cur = conn.cursor()
#     cur.execute(query)
#     try:
#         db_return = cur.fetchall()  # nested: [('c_custkey'),('c_acctbal)]
#     except psycopg2.ProgrammingError:  # if no results
#         db_return = 0
#     cur.close()
#     conn.close()
#     return db_return

def scale(nextlist, code):
    global DBNAME
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()

    for scale in [1, 10]: # CONFIG THIS
        logger.info(f"{scale=}")
        DBNAME=f'tpch{scale}'
        subres_df = nextf(nextlist[:], code)
        subres_df["scale"] = scale
        res_df = res_df.append(subres_df)

    return res_df


# FIX CONNSTR IF NEEDED
# def index(nextlist, code):
#     nextf = nextlist.pop()
#     res_df = pandas.DataFrame()
# 
#     for indexing in ["false", "true"]:
#         logger.info(f"{indexing=}")
#         db_return = exec_sql(f"call set_indexes({indexing});")
# 
#         subres_df = nextf(nextlist[:], code)
#         subres_df["index"] = indexing
#         res_df = res_df.append(subres_df)
# 
#     return res_df

def user(nextlist, code):
    global USER
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()

    for cur_user in ["root", "disable_nestloop_user"]:
        USER = cur_user
        logger.info(f"{USER=}")

        subres_df = nextf(nextlist[:], code)
        subres_df["user"] = cur_user
        res_df = res_df.append(subres_df)

    return res_df


def net(nextlist, code):
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()
    # reset any rules before starting
    shape_traffic("loc")
    for area in ["lan", "wan", "loc"]:
        logger.info(f"{area=}")

        shape_traffic(area)
        subres_df = nextf(nextlist[:], code)
        subres_df["net"] = area
        res_df = res_df.append(subres_df)

    return res_df

def optimizers(nextlist):
    global BENCH_DIR
    global BENCHMARKER_TYPE
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()

    dirs = os.listdir(BENCHMARKER_TYPE) # relative paths
    for optimizer in dirs:
        BENCH_DIR = f"{BENCHMARKER_TYPE}/{optimizer}/" # global
        logger.info(f"{BENCH_DIR=}")
        subres_df = nextf(nextlist[:])
        subres_df["optimizer"] = optimizer
        res_df = res_df.append(subres_df)

    return res_df

def wflows(nextlist):
    files = os.listdir(BENCH_DIR)
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()
    for f in files:
        logger.info(f"{f=}")
        with open(BENCH_DIR + f, "r") as file_source:
            code = file_source.read()

        subres_df = nextf(nextlist[:], code)
        subres_df["wflow"] = f
        res_df = res_df.append(subres_df)

    return res_df


def basic_bench(nextlist, code):

    all_reps = []
    connstr=CONN_TEMPLATE.format(dbname=DBNAME, user=USER, password=USER)
    for rep in range(C_TIMES):
        logger.info(f"{rep=}")
        rep_stats: pandas.DataFrame = mon.monitor(code,{"CONNSTR":connstr}, {})
        rep_stats['rep'] = rep

    return rep_stats


def bench_all(nextlist, *args):
    return nextlist.pop()(nextlist, *args)


def micro_main():

    global CONN_TEMPLATE 
    CONN_TEMPLATE='postgresql://{user}:{password}@localhost/{dbname}' 
    benchlist = [basic_bench, user, net, scale, wflows, optimizers]
    global BENCHMARKER_TYPE
    BENCHMARKER_TYPE = "benchmarks-micro"

    report = bench_all(benchlist)
    current_date = datetime.now().strftime('%m-%d--%H-%M')
    report_filename = f"micro-bench{current_date}.feather"

    report.reset_index(drop=True, inplace=True)
    report.to_feather(report_filename, compression='uncompressed')
    print(report)

def kaggle_main():
    global CONN_TEMPLATE 
    CONN_TEMPLATE = 'postgresql://{user}:{password}@localhost/module4' 
    shorterlist = [basic_bench, user, net, wflows, optimizers]
    global BENCHMARKER_TYPE
    BENCHMARKER_TYPE = "benchmarks-kaggle"

    report = bench_all(shorterlist)
    current_date = datetime.now().strftime('%m-%d--%H-%M')
    report_filename = f"kaggle-bench{current_date}.feather"

    report.reset_index(drop=True, inplace=True)
    report.to_feather(report_filename, compression='uncompressed')
    print(report)

