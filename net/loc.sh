#!/bin/bash

ERR="$(sudo tc qdisc del dev lo root 2>&1 > /tmp/loshout)"
OUT=$(</tmp/loshout)
echo "$OUT"
echo "$ERR"
if [[ "$ERR" == "Error: Cannot delete qdisc with handle of zero." || "$ERR" == "" ]];then
    exit 0
else
    exit 1
fi
