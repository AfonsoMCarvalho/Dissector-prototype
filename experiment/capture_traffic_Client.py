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
    cmd = 'sudo tcpdump -i ' + NETWORK_INTERFACE + ' -C 2000 -w ' + capture_folder + sample_name + '_client.pcap'
    #May configure -s96 as an option to gather packet to 96 B snaplen
    print(cmd)
    sub.Popen(cmd, shell=True)
    

def stop_capture(capture_folder, sample_name):
    cmd = 'tcpdump -i ' + NETWORK_INTERFACE + ' -C 2000 -w ' + capture_folder + sample_name + '_client.pcap'
    os.system('sudo pkill -15 -f "'+cmd+'"')
    print('sudo pkill -15 -f "'+cmd+'"')


def stop_capture_all():
    os.system("sudo pkill -15 -f tcpdump")


@app.route('/startTrafficCapture', methods=['POST'])
def start_traffic_capture():
    capture_folder, sample_name = str(request.data.decode("utf-8")).split(",")
    capture_traffic(capture_folder, sample_name)
    print("Starting Traffic Capture - " + capture_folder + sample_name)
    return "Starting Traffic Capture - " + capture_folder + sample_name


@app.route('/stopTrafficCapture', methods=['POST'])
def stop_traffic_capture():
    if len(str(request.data.decode("utf-8")).split(",")) > 0:
        capture_folder, sample_name = str(request.data.decode("utf-8")).split(",")
        stop_capture(capture_folder, sample_name)
    else:
        stop_capture_all()
    print("Stopping Traffic Capture")
    return "Stopping Traffic Capture"


if __name__ == "__main__":

    hostname = socket.gethostname()

    app.run(debug=False, host='0.0.0.0', port=5005)
