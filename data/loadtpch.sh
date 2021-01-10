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
\COPY customer FROM 'customer.tbl' WITH DELIMITER '|';
\COPY lineitem FROM 'lineitem.tbl' WITH DELIMITER '|';
\COPY nation FROM 'nation.tbl' WITH DELIMITER '|';
\COPY orders FROM 'orders.tbl' WITH DELIMITER '|';
\COPY part FROM 'part.tbl' WITH DELIMITER '|';
\COPY partsupp FROM 'partsupp.tbl' WITH DELIMITER '|';
\COPY region FROM 'region.tbl' WITH DELIMITER '|';
\COPY supplier FROM 'supplier.tbl' WITH DELIMITER '|';
EOF

