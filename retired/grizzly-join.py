import sqlite3

import re

import grizzly
from grizzly.aggregates import AggregateType
from grizzly.sqlgenerator import SQLGenerator
from grizzly.relationaldbexecutor import RelationalExecutor

c = sqlite3.connect("./grizzly.db")
grizzly.use(RelationalExecutor(c, SQLGenerator("sqlite")))

df = grizzly.read_table("events") 
df = df[df['globaleventid'] == 470259271]

df2 = grizzly.read_table("events")

joined = df.join(other = df2, on=["globaleventid", "globaleventid"], how = "inner")
joined.show(pretty=True)

actual = joined.generateQuery()
# expected = "SELECT * FROM events $t1 inner join events $t2 ON $t1.globaleventid = $t2.globaleventid where $t1.globaleventid = 470259271"
expected = "select * from (select * from (select * from events $t0) $t1 where $t1.globaleventid = 470259271) $t4 inner join (select * from events $t2) $t5 on $t4.globaleventid = $t5.globaleventid"

grizzly.close()
