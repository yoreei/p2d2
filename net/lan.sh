#!/bin/bash
/vagrant/net/loc.sh

sudo tc qdisc add dev lo root netem delay 0.3ms rate 1000mbit
