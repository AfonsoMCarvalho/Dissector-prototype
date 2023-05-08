import calendar
import sys, os
import subprocess as sub
import time, sched
import random
import threading
import requests
import socket
from flask import Flask
from flask import request

NETWORK_INTERFACE = "docker0"

app = Flask(__name__)

def capture_traffic(capture_folder, sample_name):
    if not os.path.exists(capture_folder):
        os.makedirs(capture_folder)

    print("Starting Traffic Capture - " + capture_folder + sample_name)
    cmd = 'sudo tcpdump -i ' + NETWORK_INTERFACE + ' -C 2000 -w ' + capture_folder + sample_name + '_hs.pcap'
    #May configure -s96 as an option to gather packet to 96 B snaplen
    print(cmd)
    sub.Popen(cmd, shell=True)

def stop_capture(capture_folder, sample_name):
    cmd = 'tcpdump -i ' + NETWORK_INTERFACE + ' -C 2000 -w ' + capture_folder + sample_name + '_hs.pcap'
    os.system('sudo pkill -15 -f "'+cmd+'"')
    print('sudo pkill -15 -f "'+cmd+'"')

def stop_capture_all():
    os.system("sudo pkill -15 -f tcpdump")


@app.route('/startTrafficCapture', methods=['POST'])
def start_traffic_capture():
    if len(str(request.data.decode("utf-8")).split(",")) > 2:
        capture_folder, sample_name, capture_time = str(request.data.decode("utf-8")).split(",")
        while calendar.timegm(time.gmtime()) < float(capture_time):
            time.sleep(1)
    else: 
        capture_folder, sample_name = str(request.data.decode("utf-8")).split(",")
    
    capture_traffic(capture_folder, sample_name)

    return "Starting Traffic Capture - " + capture_folder + sample_name


@app.route('/stopTrafficCapture', methods=['POST'])
def stop_traffic_capture():
    if len(str(request.data.decode("utf-8")).split(",")) > 0:
        capture_folder, sample_name = str(request.data.decode("utf-8")).split(",")
        stop_capture(capture_folder, sample_name)
    else:
        stop_capture_all()
    return "Stopping Traffic Capture"


if __name__ == "__main__":

    page = sys.argv[1]

    hostname = socket.gethostname()

    # docker kill $(docker ps -q)
    os.system('docker container stop torp-onion-service')
    os.system('docker container rm torp-onion-service')

    capture_traffic('pcap-folder/full-onion/', hostname + '_' + page)

    os.system('docker run -it -v /home/afonso_carvalho/hidden-service-docker-image/web:/web -p 8080:8080 --entrypoint /serve.sh -d --name torp-onion-service torp-onion-service')
    #os.system('docker run -it --rm -v /home/afonso_carvalho/hidden-service-docker-image/web:/web2 -p 8080:8080 --entrypoint /serve.sh -d --name torp-onion-service torp-onion-service')

    app.run(debug=False, host='0.0.0.0', port=5005)
