#!/usr/bin/env bash

sudo apt-get update
#dependencies
cat ubuntu.txt | xargs sudo apt-get install -y
sudo python3 -m pip install -r requirements.txt

#postgres setup
sudo -u postgres psql<<EOF
CREATE USER ${USER} WITH SUPERUSER PASSWORD '${USER}';
CREATE USER p2d2 WITH SUPERUSER PASSWORD 'p2d2';
CREATE DATABASE ${USER};
CREATE DATABASE p2d2;
EOF
#alternative way:
##createuser --superuser vagrant
##createdb vagrant

mkdir ~/bin
ln -s /vagrant/p2d2/astpp.py /home/vagrant/bin/astpp

echo export PYTHONPATH=/vagrant/grizzly/:/vagrant/ >> ~/.bashrc
echo alias pd=\'python3 -m pdb -c continue\' >> ~/.bashrc
