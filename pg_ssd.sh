sudo su

# PLEASE DO 2prep_indexes
# copy and load module4 dump
cd /vagrant/data
scp module4.sql ubuntu@ec2:/vagrant/data/module4.sql
psql module4 < module4.sql

psql
REINDEX DATABASE


# verify we can access the ssds:

lspci

lsmod | grep nvme

cat /lib/modules/$(uname -r)/modules.builtin | grep nvme

# move existing db aside if necessary
sudo service postgresql stop

mv /var/lib/postgresql /var/lib/postgresql.ebsbackup

# mount the ssds
mkfs -t ext4 /dev/nvme1n1

mkdir /var/lib/postgresql

mount /dev/nvme1n1 /var/lib/postgresql

rsync -av /var/lib/postgresql.ebsbackup/ /var/lib/postgresql

service postgresql start
service postgresql status

# test things working
psql
SHOW data_directory;
\l
\d

# run the benchmarker

cd /vagrant
python3 -m p2d2 micro
python3 -m p2d2 kaggle
