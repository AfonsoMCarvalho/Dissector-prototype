#!/bin/bash
#Run python script
echo "Request per session: $1"
echo "Sessions: $2"
echo "IP: $3"
mkdir logs
docker run -it -v /home/afonso_carvalho/logs:/logs -d --name=probe-container --entrypoint /main.sh probe-image:latest $1 $2 $3
echo "finished"