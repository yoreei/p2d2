#!/bin/bash
set -u # or set -o nounset
: "$CODEDIR"

#build tpch
echo cloning tpch-kit to ~/tpch...
git clone https://github.com/gregrahn/tpch-kit.git ~/tpch
cd ~/tpch/dbgen
make MACHINE=LINUX DATABASE=POSTGRESQL
export DSS_CONFIG=~/tpch/dbgen
export DSS_QUERY="$DSS_CONFIG"/queries

for scale in 1 10
do
    DBNAME=tpch"${scale}"
    rm -r "${CODEDIR}"/data/"${DBNAME}"
    mkdir "${CODEDIR}"/data/"${DBNAME}"
    export DSS_PATH="${CODEDIR}"/data/"${DBNAME}"
    echo generating scale "${scale}"
    ./dbgen -vf -s "${scale}"
    cp dss.ddl "${CODEDIR}"/data/tpch_dss.ddl # not needed?
    echo creating "${DBNAME}"...
    sudo -u postgres psql <<EOF
    DROP DATABASE IF EXISTS "${DBNAME}";
    CREATE DATABASE "${DBNAME}";
EOF

    echo importing dss.ddl
    sudo -u postgres psql <<EOF
    \c "${DBNAME}";
    $(<dss.ddl)
EOF

    #copy data to tables
    for file in "${CODEDIR}"/data/"${DBNAME}"/*
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
CREATE INDEX IDX_SUPPLIER_NATION_KEY ON SUPPLIER (S_NATIONKEY);

CREATE INDEX IDX_PARTSUPP_PARTKEY ON PARTSUPP (PS_PARTKEY);
CREATE INDEX IDX_PARTSUPP_SUPPKEY ON PARTSUPP (PS_SUPPKEY);

CREATE INDEX IDX_CUSTOMER_NATIONKEY ON CUSTOMER (C_NATIONKEY);

CREATE INDEX IDX_ORDERS_CUSTKEY ON ORDERS (O_CUSTKEY);

CREATE INDEX IDX_LINEITEM_ORDERKEY ON LINEITEM (L_ORDERKEY);
CREATE INDEX IDX_LINEITEM_PART_SUPP ON LINEITEM (L_PARTKEY,L_SUPPKEY);

CREATE INDEX IDX_NATION_REGIONKEY ON NATION (N_REGIONKEY);


-- aditional indexes

CREATE INDEX IDX_LINEITEM_SHIPDATE ON LINEITEM (L_SHIPDATE, L_DISCOUNT, L_QUANTITY);

CREATE INDEX IDX_ORDERS_ORDERDATE ON ORDERS (O_ORDERDATE);
EOF

    # untested
    for udf in /vagrant/sql/*
    do
        sudo -u postgres psql "${DBNAME}" < "${udf}"
    done

done
