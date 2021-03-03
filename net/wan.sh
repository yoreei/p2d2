#!/bin/bash
/vagrant/net/loc.sh

sudo tc qdisc add dev eth0 root netem delay 25ms rate 100mbit loss 1%
