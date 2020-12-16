#!/usr/bin/env bash

sudo apt-get update
#dependencies
sudo apt-get install -y python3-pip postgresql postgresql-contrib
sudo apt-get install -y libpq-dev #psychopg2 compile dependency
pip3 install psycopg2 grizzly-sql modin[ray] scikit-learn
pip3 install beautifultable #grizzly test dep

#postgres setup
sudo -u postgres psql<<EOF
CREATE USER vagrant WITH SUPERUSER PASSWORD 'vagrant';
CREATE DATABASE vagrant;
EOF
#alternative way:
##createuser --superuser vagrant
##createdb vagrant



mkdir /home/vagrant/bin
ln -s /vagrant/p2d2/astpp.py /home/vagrant/bin/astpp


rm ~/.bashrc
echo export PYTHONPATH=$PYTHONPATH:/vagrant/p2b2/p2b2 >> ~/.bashrc
echo alias ls=\'ls -F\' >> ~/.bashrc
echo alias pd=\'python3 -m pdb -c continue\' >> ~/.bashrc
#sudo apt-get install -y vim ack ack-grep git
