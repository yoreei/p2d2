import time

start_clock = time.perf_counter()
import pandas as pd
import numpy as np

### DEBUG
# CONNSTR='postgresql://root:root@localhost/tpch1'
# from types import SimpleNamespace
# SHARED_DB_TIME=SimpleNamespace()
### END DEBUG


def udf_disc_price(extended, discount):
    import numpy as np

    return np.multiply(extended, np.subtract(1, discount))


def udf_charge(extended, discount, tax):
    import numpy as np

    return np.multiply(extended, np.multiply(np.subtract(1, discount), np.add(1, tax)))


lineitem = pd.read_sql(
    "SELECT * FROM lineitem",
    parse_dates=["l_shipdate", "l_commitdate", "l_receiptdate"],
    con=CONNSTR,
)
# SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock

lineitem = lineitem.astype({"l_returnflag": "category", "l_linestatus": "category"})

df = lineitem[
    [
        "l_shipdate",
        "l_returnflag",
        "l_linestatus",
        "l_quantity",
        "l_extendedprice",
        "l_discount",
        "l_tax",
    ]
][(lineitem["l_shipdate"] <= "1998-09-01")]
df["disc_price"] = udf_disc_price(df["l_extendedprice"], df["l_discount"])
df["charge"] = udf_charge(df["l_extendedprice"], df["l_discount"], df["l_tax"])
result = df.groupby(["l_returnflag", "l_linestatus"]).agg(
    {
        "l_quantity": "sum",
        "l_extendedprice": "sum",
        "disc_price": "sum",
        "charge": "sum",
        "l_quantity": "mean",
        "l_extendedprice": "mean",
        "l_discount": "mean",
        "l_shipdate": "count",
    }
)

SHARED_WALL_TIME.value = time.perf_counter() - start_clock
print(time.perf_counter() - start_clock)
print(f"{result=}")
print(f"{len(result)=}")
