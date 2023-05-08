import os, sys
import subprocess as sub
import logging
import time
import random
import socket
from datetime import datetime
import argparse
import numpy as np

from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager


# python3 job_coordinator_scale_tor.py

    

def run_experiment():
    
    random.seed(42)

    print("[#] Starting job coordinator server...")
    sub.Popen("python3 job_coordinator_server_scale_tor.py", shell=True)

    print("####################################")
    print("[#] Running experiments")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Start time: ", dt_string)	
    print("####################################")
    
    print("[#] Installing packages in onion and client machines...")
    sub.call("ansible-playbook run_collection.yml  --tags \"setup_packages\"", shell=True)

    print("[#] Running experiment config ansible tasks...")
    sub.call("ansible-playbook run_collection.yml  --tags \"config_exp\"", shell=True)

    print("[#] Setting up onion service in container...")
    sub.call("ansible-playbook run_collection.yml  --tags \"setup_onion\"", shell=True)

    print("[#] Transfering onion real pages...")
    sub.call("ansible-playbook run_collection.yml  --tags \"upload_real_onion_pages\"", shell=True)
  
    print("[#] Start captures...")
    sub.call("ansible-playbook run_collection.yml  --tags \"start_capture\"", shell=True)

    #wait 1:30 min to make sure OS is fully published
    print("[#] Waiting for Onions to fully initialize...")
    time.sleep(90)

    print("[#] Running experiment...")
    sub.call("ansible-playbook run_collection.yml  --tags \"run_exp\"", shell=True)
    
    # Multiple clients handled in job coordinator server
    print("[#] Waiting for experiment to finish...")
    while(not os.path.exists("terminator")):
        time.sleep(5)

    os.system("rm terminator")

    print("[#] Found final terminator for !")
    print("[#] Experiment finished! Cleaning screens...")
    sub.call("ansible-playbook run_collection.yml  --tags \"kill_screens\"", shell=True)

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("End time: ", dt_string)
    time.sleep(5)

    print("[#] Killing job coordinator server...")
    os.system("pkill -9 -f job_coordinator_server_scale_tor.py")


    print("[*] Fetching experiment results...")
    sub.call("ansible-playbook run_collection.yml  --tags \"fetch_all_pcaps\"", shell=True)

    print("[*] Cleanup experiment results...")
    sub.call("ansible-playbook run_collection.yml  --tags \"rm_pcaps\"", shell=True)



if __name__ == "__main__":

    run_experiment()