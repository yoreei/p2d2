#!/usr/bin/env python3
"""
Produces csv reports from microbenchmarks
"""
import subprocess
import functools
import importlib
import ast
import os

import astunparse
import pandas
import psycopg2

import p2d2.optimizer as optimizer
from . import argparse_factory
from . import logrotate
from . import log
from . import monitor

logger = log.getLogger(__name__)

C_TIMES = 2
CONNSTRTEMPLATE = "host=localhost dbname=tpch{} user=postgres password=postgres"
CONNSTR = CONNSTRTEMPLATE.format(1)
CMD_ARGS = argparse_factory.parse_args()


def shape_traffic(area: str):

    child = subprocess.Popen(["/bin/bash", f"./net/{area}.sh"])
    child.communicate()
    rc = child.returncode
    assert rc == 0
    return rc


def exec_sql(query):
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


def change_conn(parsetree, newconn):
    for node in parsetree.body:
        if (
            type(node) == ast.Assign
            and type(node.value) == ast.Call
            and type(node.value.func) == ast.Attribute
            and node.value.func.attr == "connect"
            and type(node.value.func.value) == ast.Name
            and node.value.func.value.id == "psycopg2"
        ):
            print("got it")
            logger.debug("change_conn found {node}")
            node.value.args[0].values[0].value = newconn
    return parsetree


def warm_up(bytecode, times):
    for _ in range(times):
        exec(bytecode)


def ver(nextlist, parsetree):
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()
    global optimizer
    res_df = pandas.DataFrame()
    for ver in ["p2d2.optimizer", "p2d2.no_optimizer"]:
        # print(f'ver {ver}')
        logger.info(f"{ver=}")

        optimizer = importlib.import_module(ver)

        subres_df = nextf(nextlist[:], parsetree)

        subres_df["ver"] = ver
        res_df = res_df.append(subres_df)

    return res_df


def scale(nextlist, parsetree):

    nextf = nextlist.pop()
    res_df = pandas.DataFrame()

    for scale_num in [1, 10]:
        # print(f'**scale {scale_num}')
        logger.info(f"{scale_num=}")

        CONNSTR = CONNSTRTEMPLATE.format(scale_num)
        parsetree = change_conn(parsetree, CONNSTR)
        subres_df = nextf(nextlist[:], parsetree)
        subres_df["scale"] = scale_num
        res_df = res_df.append(subres_df)

    return res_df


def index(nextlist, parsetree):
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()

    for indexing in ["true", "false"]:
        # print(f'**index {indexing}')
        logger.info(f"{indexing=}")
        db_return = exec_sql(f"call set_indexes({indexing});")

        subres_df = nextf(nextlist[:], parsetree)
        subres_df["index"] = indexing
        res_df = res_df.append(subres_df)

    return res_df


def net(nextlist, parsetree):
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()
    # reset any rules before starting
    shape_traffic("loc")
    for area in ["lan", "wan", "loc"]:
        print(f"**{area}")
        logger.info(f"{area=}")

        shape_traffic(area)
        subres_df = nextf(nextlist[:], parsetree)
        subres_df["net"] = area
        res_df = res_df.append(subres_df)

    return res_df


def wflows(nextlist):
    DIR = "microbenchmarks/"
    if CMD_ARGS.infile:
        files = CMD_ARGS.infile
    else:
        files = os.listdir(DIR)
    nextf = nextlist.pop()
    res_df = pandas.DataFrame()
    visible_files = filter(lambda x: not x.startswith("."), files)
    for f in visible_files:
        with open(DIR + f, "r") as file_source:
            parsetree = ast.parse(file_source.read())

        subres_df = nextf(nextlist[:], parsetree)
        subres_df["wflow"] = f
        res_df = res_df.append(subres_df)

    return res_df


def basic_bench(nextlist, parsetree):
    opt_parsetree, opt_time = monitor.timeit(optimizer.optimize, parsetree, CONNSTR)

    # opt_bcode = compile(opt_parsetree, 'str', 'exec')
    opt_code = astunparse.unparse(opt_parsetree)
    mon = monitor.Monitor(exec, opt_code)

    # breakpoint()
    time_incl = []
    for i in range(C_TIMES):
        time_incl += [
            {
                "oom": mon.oom,
                "opt_time": opt_time,
                "rep": i,
                "wall_time": mon.time,
                "cpu_utilization": 0,
                "mem_usage": mon.diffs,
                "net_usage": 0,
            }
        ]
        # print(time_incl[-1])

    return pandas.DataFrame(time_incl)


def bench_all(nextlist, *args):
    return nextlist.pop()(nextlist, *args)


def main():
    benchlist = [basic_bench, ver, index, net, scale, wflows]

    report = bench_all(benchlist)
    logrotate.write(report, "./docs/microbenchmarks.csv")
    print(report)


if __name__ == "__main__":
    main()
