#!/bin/bash

for dbname in {tpch1,tpch10,tpch100,module4}
do
    sudo psql --dbname="${DBNAME}"<<EOF
$(</vagrant/sql/enable_indexes.sql)

EOF
done
