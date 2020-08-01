#!/bin/bash
for i in `nmap -sL 192.168.0.0/24 | grep ESP | grep -oE "([0-9]{1,3}[\.]){3}[0-9]{1,3}"`;
do
    echo $i;
    python3 water.py  $i -t 180;
done
