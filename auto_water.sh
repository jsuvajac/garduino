#!/bin/bash
date
python3 water.py  192.168.0.40 -t 180
if [ $? -ne 0 ]
then
  echo "Could not reach esp"
fi
echo ""