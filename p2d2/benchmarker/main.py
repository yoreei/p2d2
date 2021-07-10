#!/usr/bin/env python3
"""
Produces csv reports from microbenchmarks
"""
import subprocess
from datetime import datetime

import pandas
from pathlib import Path

from . import log
from . import monitor as mon

logger = log.getLogger(__name__)


def shape_traffic(area: str):
    child = subprocess.Popen(["/bin/bash", f"./net/{area}.sh"])
    child.communicate()
    rc = child.returncode
    assert rc == 0
    return rc


def write(df, name) -> None:
    df.reset_index(drop=True, inplace=True)
    df.to_feather(name + ".feather", compression="uncompressed")


def columnize(df, **kwargs) -> None:
    for key, value in kwargs.items():
        df[key] = value


def kaggle_main():
    pass


def micro_main():
    """
    1.{5end_to_end} tpch 1,2,3,4,5 with scale 1, 10
    2 {5module4} and 3. module4 | also {5module4mem} and {5module4net}
    3.{5tpchmodin} tpch 1, 4, 5 with modin on scale 10
    4.{5micro_scales} micros with scale 1, 10 | also {5micro_traffic}
    5.{5micro_net} micro join, selection with net=wan and scale 1
    """

    def one():
        name = "5end_to_end"
        print(name)
        path = Path("benchmarks-micro")
        result = pandas.DataFrame()
        for wflow in ["tpch2.py", "tpch3.py", "tpch1.py", "tpch4.py", "tpch5.py"]:
            for optimizer in ["base", "optimized"]:
                with open(path / optimizer / wflow, "r") as file_source:
                    code = file_source.read()

                connstr = "postgresql://root:root@localhost/tpch1"
                logger.info(f"{wflow} {optimizer} {connstr}")
                curr_df: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})
                columnize(curr_df, wflow=wflow, optimizer=optimizer, scale=1, net="loc")
                result = result.append(curr_df)

                connstr = "postgresql://root:root@localhost/tpch10"
                logger.info(f"{wflow} {optimizer} {connstr}")
                curr_df: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})
                columnize(
                    curr_df, wflow=wflow, optimizer=optimizer, scale=10, net="loc"
                )
                result = result.append(curr_df)

        write(result, name)

    def two():
        name = "5module4"
        print(name)
        path = Path("benchmarks-kaggle")
        wflow = "module4.py"
        result = pandas.DataFrame()
        for optimizer in ["base", "optimized"]:
            with open(path / optimizer / wflow, "r") as file_source:
                code = file_source.read()

            connstr = "postgresql://disable_nestloop_user:disable_nestloop_user@localhost/module4"
            logger.info(f"{wflow} {optimizer} {connstr}")
            curr_df: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})
            columnize(curr_df, wflow=wflow, optimizer=optimizer, scale=1, net="loc")
            result = result.append(curr_df)

        write(result, name)

    def three():
        name = "5tpchmodin"
        print(name)
        path = Path("benchmarks-micro")
        result = pandas.DataFrame()
        for wflow in ["tpch1.py", "tpch4.py", "tpch5.py"]:
            optimizer = "modin"
            with open(path / optimizer / wflow, "r") as file_source:
                code = file_source.read()

            connstr = "postgresql://root:root@localhost/tpch10"
            logger.info(f"{wflow} {optimizer} {connstr}")
            curr_df: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})
            columnize(curr_df, wflow=wflow, optimizer=optimizer, scale=10, net="loc")
            result = result.append(curr_df)

        write(result, name)

    def four():
        name = "5micro_scales"
        print(name)
        path = Path("benchmarks-micro")
        result = pandas.DataFrame()
        for wflow in ["micro_join.py", "micro_sel.py", "micro_proj.py", "micro_max.py"]:
            for optimizer in ["optimized", "base"]:
                with open(path / optimizer / wflow, "r") as file_source:
                    code = file_source.read()

                connstr = "postgresql://root:root@localhost/tpch1"
                logger.info(f"{wflow} {optimizer} {connstr}")
                curr_df: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})
                columnize(curr_df, wflow=wflow, optimizer=optimizer, scale=1, net="loc")
                result = result.append(curr_df)

                connstr = "postgresql://root:root@localhost/tpch10"
                logger.info(f"{wflow} {optimizer} {connstr}")
                curr_df: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})
                columnize(
                    curr_df, wflow=wflow, optimizer=optimizer, scale=10, net="loc"
                )
                result = result.append(curr_df)

        write(result, name)

    def five():
        name = "5micro_net"
        print(name)
        path = Path("benchmarks-micro")
        result = pandas.DataFrame()
        for wflow in ["micro_join.py", "micro_sel.py", "micro_proj.py", "micro_max.py"]:
            for optimizer in ["optimized", "base"]:
                with open(path / optimizer / wflow, "r") as file_source:
                    code = file_source.read()

                connstr = "postgresql://root:root@localhost/tpch1"

                # wan
                logger.info(f"wan {wflow} {optimizer} {connstr}")
                shape_traffic("wan")
                curr_df: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})
                shape_traffic("loc")
                columnize(
                    curr_df, wflow=wflow, optimizer=optimizer, scale=1, net="wan"
                )
                result = result.append(curr_df)

                # lan
                logger.info(f"lan {wflow} {optimizer} {connstr}")
                shape_traffic("lan")
                curr_df: pandas.DataFrame = mon.monitor(code, {"CONNSTR": connstr}, {})
                shape_traffic("loc")
                columnize(
                    curr_df, wflow=wflow, optimizer=optimizer, scale=1, net="lan"
                )
                result = result.append(curr_df)

        write(result, name)

    shape_traffic("loc")
    five()
