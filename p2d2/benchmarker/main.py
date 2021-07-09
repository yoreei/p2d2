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


def shape_traffic(area: str):
    child = subprocess.Popen(["/bin/bash", f"./net/{area}.sh"])
    child.communicate()
    rc = child.returncode
    assert rc == 0
    return rc


def write(df, name):
    df.reset_index(drop=True, inplace=True)
    df.to_feather(name + ".feather", compression="uncompressed")


def micro_main():
    """
    1.{5end_to_end} tpch 1,2,3,4,5 with scale 1, 10
    2 {5module4} and 3. module4 | also {5module4mem} and {5module4net}
    3.{5tpchmodin} tpch 1, 4, 5 with modin on scale 10
    4.{5micro_scales} micros with scale 1, 10
    5.{5micro_net} micro join, selection with net=wan and scale 1
    """

    def one():
        name = "5end_to_end"
        print(name)
        path = Pathlib("benchmarks-micro")
        for f in ["tpch1.py", "tpch2.py", "tpch3.py", "tpch4.py", "tpch5.py"]:
            for bench_dir in ["base", "optimized"]:
                with open(path / bench_dir / f, "r") as file_source:
                    code = file_source.read()

                connstr = "postgresql://root:root@localhost/tpch1"
                print(f, bench_dir, connstr)
                result: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})

                connstr = "postgresql://root:root@localhost/tpch10"
                print(f, bench_dir, connstr)
                scale10: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})

                result = result.append(scale10)
                write(result, name)

    def two():
        name = "5module4"
        print(name)
        path = Pathlib("benchmarks-kaggle")
        f = "module4"
        for bench_dir in ["base", "optimized"]:
            with open(path / bench_dir / f, "r") as file_source:
                code = file_source.read()

            connstr = "postgresql://root:root@localhost/module4"
            print(f, bench_dir, connstr)
            result: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})

            write(result, name)

    def three():
        print("5tpchmodin")
        path = Pathlib("benchmarks-kaggle")
        for f in ["tpch1.py", "tpch4.py", "tpch5.py"]:
            bench_dir = "modin"
            with open(path / bench_dir / f, "r") as file_source:
                code = file_source.read()

            connstr = "postgresql://root:root@localhost/tpch10"
            print(f, bench_dir, connstr)
            result: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})

            write(result, name)

    def four():
        print("5micro_scales")
        path = Pathlib("benchmarks-micro")
        for f in ["micro_join.py", "micro_sel.py", "micro_proj.py", "micro_max.py"]:
            for bench_dir in ["optimized", "base"]:
                with open(path / bench_dir / f, "r") as file_source:
                    code = file_source.read()

                connstr = "postgresql://root:root@localhost/tpch1"
                print(f, bench_dir, connstr)
                result: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})

                connstr = "postgresql://root:root@localhost/tpch10"
                print(f, bench_dir, connstr)
                scale10: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})

                result = result.append(scale10)
                write(result, name)

    def five():
        print("5micro_net")
        path = Pathlib("benchmarks-micro")
        for f in ["micro_join.py", "micro_sel.py"]:
            for bench_dir in ["optimized", "base"]:
                with open(path / bench_dir / f, "r") as file_source:
                    code = file_source.read()

                connstr = "postgresql://root:root@localhost/tpch1"
                print(f, bench_dir, connstr)
                shape_traffic("wan")
                result: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})
                shape_traffic("loc")

                write(result, name)

    shape_traffic("loc")
    one()
