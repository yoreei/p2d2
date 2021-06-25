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

C_TIMES = 2
# default value used for shorter pipelines runs


def shape_traffic(area: str):

    child = subprocess.Popen(["/bin/bash", f"./net/{area}.sh"])
    child.communicate()
    rc = child.returncode
    assert rc == 0
    return rc

def exec_sql(query):
    global CONNSTR
    conn = psycopg2.connect(CONNSTR)
    cur = conn.cursor()
    cur.execute(query)
    try:
        db_return = cur.fetchall()  # nested: [('c_custkey'),('c_acctbal)]
    except psycopg2.ProgrammingError:  # if no results
        db_return = 0
    cur.close()
    conn.close()
    return db_return

def scale(nextlist, code):
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()

    for scale in [1, 10]:
        logger.info(f"{scale=}")
        global CONNSTR
        CONNSTR = f"host=localhost dbname=tpch{scale} user=p2d2 password=p2d2"
        subres_df = nextf(nextlist[:], code)
        subres_df["scale"] = scale
        res_df = res_df.append(subres_df)

    return res_df


def index(nextlist, code):
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()

    for indexing in ["true", "false"]:
        logger.info(f"{indexing=}")
        db_return = exec_sql(f"call set_indexes({indexing});")

        subres_df = nextf(nextlist[:], code)
        subres_df["index"] = indexing
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
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()

    dirs = os.listdir(BENCHMARK_TYPE) # relative paths
    for optimizer in dirs:
        BENCH_DIR = f"{BENCHMARK_TYPE}/{optimizer}/" # global
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
    for rep in range(C_TIMES):
        logger.info(f"{rep=}")
        rep_stats: pandas.DataFrame = mon.monitor(code,{"CONNSTR":CONNSTR}, {})
        rep_stats['rep'] = rep

    return rep_stats


def bench_all(nextlist, *args):
    return nextlist.pop()(nextlist, *args)


def micro_main():
    global CONNSTR 
    CONNSTR= f"host=localhost dbname=tpch1 user=root password=root"
    benchlist = [basic_bench, index, net, scale, wflows, optimizers]
    global BENCHMARKER_TYPE
    BENCHMARKER_TYPE = "benchmarks"

    report = bench_all(benchlist)
    current_date = datetime.now().strftime('%m-%d--%H-%M')
    report_filename = f"micro-bench{current_date}.feather"

    report.reset_index(drop=True, inplace=True)
    report.to_feather(report_filename, compression='uncompressed')
    print(report)

def kaggle_main():
    global CONNSTR 
    CONNSTR = f"host=localhost dbname=module4 user=root password=root"
    shorterlist = [basic_bench, wflows, optimizers]
    global BENCHMARKER_TYPE
    BENCHMARKER_TYPE = "kaggle-benchmarks"

    db_return = exec_sql(f"call set_indexes(true);")
    shape_traffic("wan")
    report = bench_all(shorterlist)
    shape_traffic("loc")
    current_date = datetime.now().strftime('%m-%d--%H-%M')
    report_filename = f"kaggle-bench{current_date}.feather"

    report.reset_index(drop=True, inplace=True)
    report.to_feather(report_filename, compression='uncompressed')
    print(report)

