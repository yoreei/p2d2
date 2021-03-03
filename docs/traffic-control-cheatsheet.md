# Traffic Control Cheatsheet

This is a page for quick reference for the tc tool.

Debian package **iproute**

Use mosh to avoid disconnects

To limit non-local traffic, replace "lo" with adapter, e.g. "eth0"

### List all active rules

```
tc qdisc show
```

### List active rules for device

```
tc qdisc show dev lo
```

# Emulate LAN

```
tc qdisc add dev lo root netem delay 0.3ms rate 1000mbit
```

# Emulate WAN

```
tc qdisc add dev lo root netem delay 25ms rate 100mbit loss 1%
```

### Delete all rules (Emulates localhost)

```
tc qdisc del dev lo root
```
