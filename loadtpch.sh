#!/bin/bash
set -u # or set -o nounset
: "$CODEDIR"

#build tpch
echo cloning tpch-kit to ~/tpch...
git clone https://github.com/gregrahn/tpch-kit.git ~/tpch
cd ~/tpch/dbgen
make MACHINE=LINUX DATABASE=POSTGRESQL
export DSS_CONFIG=~/tpch/dbgen
export DSS_QUERY=$DSS_CONFIG/queries

for scale in 1 10
do
    DBNAME=tpch${scale}
    rm -r ${CODEDIR}/data/${DBNAME}
    mkdir ${CODEDIR}/data/${DBNAME}
    export DSS_PATH=${CODEDIR}/data/${DBNAME}
    ./dbgen -vf -s ${scale}
    cp dss.ddl ${CODEDIR}/data/tpch_dss.ddl
    echo creating ${DBNAME}...
    psql <<EOF
    DROP DATABASE IF EXISTS ${DBNAME};
    CREATE DATABASE ${DBNAME};
EOF

    #create tables
    psql <<EOF
    \c ${DBNAME};
    $(<../tpch_dss.ddl)
EOF

    #copy data to tables
    for file in *
    do
        psql <<EOF
        \c ;
        \COPY ${DBNAME} FROM '${file}' WITH DELIMITER '|';
EOF
    done
done

#pgbouncer setup
echo %include ${CODEDIR}/pgbouncer.ini | sudo tee -a /etc/pgbouncer/pgbouncer.ini
psql -Atq -c "SELECT concat('\"', usename, '\" \"', passwd, '\"') FROM pg_shadow" |
    sudo tee -a /etc/pgbouncer/userlist.txt
sudo service pgbouncer restart

#indexing setup
psql<<EOF
SELECT 'CREATE INDEX ' || table_name || '_' || column_name || ' ON ' || table_name || ' ("' || column_name || '");' 
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name != 'pg_stat_statements'
  AND table_name != 'pg_buffercache';
EOF


