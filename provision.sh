#!/usr/bin/env bash
CODEDIR=/vagrant
cd ${CODEDIR}

sudo apt-get update
#dependencies
cat ubuntu.txt | xargs sudo apt-get install -y
sudo python3 -m pip install -r requirements.txt

mkdir /root/bin /home/vagrant/bin
ln -s ${CODEDIR}/p2d2/astpp.py /root/bin/astpp /home/vagrant/bin

echo "
export PYTHONPATH=${CODEDIR}/grizzly/:${CODEDIR}/
alias pd=\'python3 -m pdb -c continue\'
export CODEDIR=${CODEDIR}
"| tee -a /root/.bashrc /home/vagrant/.bashrc
sudo -u postgres psql<<eof
ALTER USER postgres WITH PASSWORD 'postgres';
eof


# deleted: just use user postgres when connecting
#sudo -u postgres psql<<EOF
#CREATE USER ${USER} WITH SUPERUSER PASSWORD '${USER}';
#CREATE USER p2d2 WITH SUPERUSER PASSWORD 'p2d2';
#CREATE DATABASE ${USER};
#CREATE DATABASE p2d2;
#EOF
