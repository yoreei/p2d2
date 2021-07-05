#!/bin/bash

echo run as root
pg_restore -C -d -w postgres module4.dump
pg_restore -C -d -w postgres tpch1.dump
pg_restore -C -d -w postgres tpch10.dump
pg_restore -C -d -w postgres tpch100.dump
