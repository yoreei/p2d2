tc qdisc add dev vmnet1 handle 1: root htb default 11
tc class add dev vmnet1 parent 1: classid 1:1 htb rate 1000Mbps
tc class add dev vmnet1 parent 1:1 classid 1:11 htb rate 512kbit
tc qdisc add dev vmnet1 parent 1:11 handle 10: netem delay 50ms
