#!/bin/bash

mkdir logs
echo "Requests p session: $1"
echo "Sessions: $2"
echo "Probe host ip: $3"
echo 'before' >> output.txt
python3 experiment.py $1 $2 $3
echo 'after' >> output.txt