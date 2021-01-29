#!/usr/bin/env bash
CODEDIR=/vagrant
cd ${CODEDIR}

sudo apt-get update
#dependencies
cat ubuntu.txt | xargs sudo apt-get install -y
sudo python3 -m pip install -r requirements.txt

#postgres setup
# creating two users for more comfortable usage:
# workflows will connect to p2d2
# interactive users (psql) will connect to ${USER}
sudo -u postgres psql<<EOF
CREATE USER ${USER} WITH SUPERUSER PASSWORD '${USER}';
CREATE USER p2d2 WITH SUPERUSER PASSWORD 'p2d2';
CREATE DATABASE ${USER};
CREATE DATABASE p2d2;
EOF
#alternative way:
##createuser --superuser ${USER}
##createdb ${USER}


mkdir ~/bin
ln -s ${CODEDIR}/p2d2/astpp.py ~/bin/astpp

echo export PYTHONPATH=${CODEDIR}/grizzly/:${CODEDIR}/ >> ~/.bashrc
echo alias pd=\'python3 -m pdb -c continue\' >> ~/.bashrc
echo export CODEDIR=${CODEDIR}>> ~/.bashrc

