#!/usr/bin/env python3
import IPython
import grizzly
import sqlite3
from grizzly.relationaldbexecutor import RelationalExecutor

con = sqlite3.connect("grizzly.db")

grizzly.use(RelationalExecutor(con))

df = grizzly.read_table("events")

df = df[df["globaleventid"] == 470747760]  # filter
df = df[["actor1name", "actor2name"]]

df.show(pretty=True)
print("1---------------------------------------")
# IPython.embed();
print(df.generate())

df1 = grizzly.read_table("t1")
df2 = grizzly.read_table("t2")

j = df1.join(
    df2,
    on=(df1.actor1name == df2.actor2name)
    | (df1["actor1countrycode"] <= df2["actor2countrycode"]),
    how="left outer",
)
cnt = j.count()
print(f"join result contais {cnt} elments")

print("2---------------------------------------")
print(j.generate())

df = grizzly.read_table("events")

print(df.count("actor2name"))

print("3---------------------------------------")
print(df.generate())

from grizzly.aggregates import AggregateType

df = grizzly.read_table("events")
g = df.groupby(["year", "actor1name"])

a = g.agg(col="actor2name", aggType=AggregateType.COUNT)
a.show()
print("4--------------------------------------")
print(a.generate())
