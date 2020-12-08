#!/bin/bash

#create db
psql <<EOF
DROP DATABASE IF EXISTS tpch;
CREATE DATABASE tpch;
EOF

#create tables
psql <<EOF
\c tpch;
$(<dss.ddl)
EOF

#copy data to tables
psql <<EOF
\c tpch;
COPY customer FROM '/vagrant/data/customer.tbl' WITH DELIMITER '|';
COPY lineitem FROM '/vagrant/data/lineitem.tbl' WITH DELIMITER '|';
COPY nation FROM '/vagrant/data/nation.tbl' WITH DELIMITER '|';
COPY orders FROM '/vagrant/data/orders.tbl' WITH DELIMITER '|';
COPY part FROM '/vagrant/data/part.tbl' WITH DELIMITER '|';
COPY partsupp FROM '/vagrant/data/partsupp.tbl' WITH DELIMITER '|';
COPY region FROM '/vagrant/data/region.tbl' WITH DELIMITER '|';
COPY supplier FROM '/vagrant/data/supplier.tbl' WITH DELIMITER '|';
EOF

