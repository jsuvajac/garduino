#!/bin/bash
for i in `nmap -sL 192.168.0.0/24 | grep ESP | grep -oE "([0-9]{1,3}[\.]){3}[0-9]{1,3}"`;
do
    python3 water_client.py  $i;
    echo $i;
done
