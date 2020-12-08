#!/usr/bin/env python3
import grizzly
import sqlite3
import IPython

con = sqlite3.connect("grizzly.db")

df = grizzly.read_table("events", con)

df.show()

IPython.embed()
