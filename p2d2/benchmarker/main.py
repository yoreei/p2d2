#!/usr/bin/env python3
"""
Produces csv reports from microbenchmarks
"""
import subprocess
import os

import pandas
import psycopg2

from . import logrotate
from . import log
from . import monitor

logger = log.getLogger(__name__)

C_TIMES = 2


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
    global DIR
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()

    DIR = "benchmarks/base/" # global
    logger.info(f"{DIR=}")
    subres_df = nextf(nextlist[:])
    subres_df["optimizer"] = "base"
    res_df = res_df.append(subres_df)

    DIR = "benchmarks/optimized/" # global
    logger.info(f"{DIR=}")
    subres_df = nextf(nextlist[:])
    subres_df["optimizer"] = "optimized"
    res_df = res_df.append(subres_df)

    DIR = "benchmarks/modin/" # global
    logger.info(f"{DIR=}")
    subres_df = nextf(nextlist[:])
    subres_df["optimizer"] = "modin"
    res_df = res_df.append(subres_df)

    return res_df

def wflows(nextlist):
    files = os.listdir(DIR)
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()
    for f in files:
        logger.info(f"{f=}")
        with open(DIR + f, "r") as file_source:
            code = file_source.read()

        subres_df = nextf(nextlist[:], code)
        subres_df["wflow"] = f
        res_df = res_df.append(subres_df)

    return res_df


def basic_bench(nextlist, code):
    logger.info(f"executing...")
    mon = monitor.Monitor(exec, code, {"CONNSTR":CONNSTR})
    # opt_time = read from metafiles

    # breakpoint()
    time_incl = []
    for i in range(C_TIMES):
        time_incl += [
            {
                "oom": mon.oom,
                # "opt_time": opt_time,
                "rep": i,
                "wall_time": mon.time,
                "cpu_utilization": 0,
                "mem_usage": mon.diffs,
                "net_usage": 0,
            }
        ]

    return pandas.DataFrame(time_incl)


def bench_all(nextlist, *args):
    return nextlist.pop()(nextlist, *args)


def main():
    benchlist = [basic_bench, index, net, scale, wflows, optimizers]

    report = bench_all(benchlist)
    report_filename = "bench_report9Jul.csv"
    logrotate.write(report, report_filename)
    # find max memory usage
    df['mem_usage']=df['mem_usage'].apply(lambda x: max(x))

    # convert to MB
    df['mem_usage']=df['mem_usage'].apply(lambda x: x//10**6)

    df.to_csv(report_filename+".max", index=False)
    print(report)


if __name__ == "__main__":
    main()
