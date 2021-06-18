#!/bin/bash
# Run this after site.yml. This script assumes that the tpch .tbl files are available on ~/bucket (presumably residing on s3 mounted with s3fs). It creates the tables in postgresql and populates them

for scale in 1 10 100
do
    DBNAME=tpch"${scale}"
    echo creating "${DBNAME}"...
    sudo -u postgres psql <<EOF
    DROP DATABASE IF EXISTS "${DBNAME}";
    CREATE DATABASE "${DBNAME}";
EOF

    echo importing dss.ddl
    sudo -u postgres psql <<EOF
    \c "${DBNAME}";
    $(</vagrant/tpch/dbgen/dss.ddl)
EOF

    #copy data to tables
    for file in ~/bucket/"${DBNAME}"/*
    do
        RELNAME=$(basename "$file" .tbl)
        echo copying "$file" to "$RELNAME"
        sudo -u postgres psql <<EOF
        \c "${DBNAME}";
        \COPY "${RELNAME}" FROM ${file} WITH DELIMITER '|';
EOF
    done
    # taken from https://github.com/tvondra/pg_tpch/blob/master/dss/tpch-index.sql
    sudo -u postgres psql<<EOF
\c "${DBNAME}"

CREATE UNIQUE INDEX IDX_ORDERS_CUSTKEY ON ORDERS (O_ORDERKEY);

CREATE UNIQUE INDEX IDX_LINEITEM_ORDERKEY ON LINEITEM (L_ORDERKEY);
CREATE UNIQUE INDEX IDX_LINEITEM_ORDERKEY ON LINEITEM (L_LINENUMBER);

EOF

    # untested
    for udf in /vagrant/sql/*
    do
        sudo -u postgres psql "${DBNAME}" < "${udf}"
    done

done
