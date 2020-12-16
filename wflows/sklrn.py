#!/bin/env python3

import sklearn
import p2d2.pgconn

conn = p2d2.pgconn.get()
print(conn)
