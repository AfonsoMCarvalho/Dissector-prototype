from http.client import REQUEST_URI_TOO_LONG
import os, sys
import subprocess as sub
import logging
import time
import calendar
import socket
import requests
import random
import tempfile
import tbselenium.common as cm
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import start_xvfb, stop_xvfb
from stem.control import Controller
from os.path import join

#logging.disable(logging.DEBUG)

logging.basicConfig(level=logging.DEBUG,filename='/logs/experiment.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

home_folder = "/home/afonso_carvalho/"
docker_home_folder = "./"
pathToTorBrowser = '/tor-browser_en-US'

NETWORK_INTERFACE = "ens4"

#seconds +1 second due to waits to ensure onion restcalls arrive before requests
time_between_requests = 2

#seconds
time_to_wait_after_tor_relaunch = 20 

def RESTCall(host, method, args=""):
    url='http://' + host + ':5005/' + method

    #Ensure that we will not continue through the experiment while
    # we do not properly communicate with onion hosts.
    #Backoff until a max of 16s between repeated requests

    r = None
    backoff = 1
    wait = 0
    while(r is None):
        try:
            r = requests.post(url, data=args, timeout=3.05)
        except requests.exceptions.RequestException as e:
            logging.debug(e)
            logging.debug("Sleeping for backoff time: %ds"%backoff)
            # It can stop here ...
            if(wait < 10):
                time.sleep(backoff)
                wait += 1
    
    return r

def place_request_via_tor(driver, os_node, request_iterations, session_sample_name):
    
    #Cycle request_iterations times through the HS list and place requests
    for i in range(request_iterations):
        logging.debug("Iteration number: %d"%i)
        print("Request number: %d"%i)
        
        # sample_name = session_sample_name + "_request_" + str(i)
        # onion_cap_folder = home_folder+"pcap-folder/" + hostname + "-" + os_node['node_name'] + "/"

        #Instruct pcap to start at the OS
        #RESTCall(os_node['ansible_host'], "startTrafficCapture", onion_cap_folder + "," + sample_name)

        #Instruct pcap to start locally
        #RESTCall(client_host_ip, "startTrafficCapture", client_cap_folder + "," + sample_name)

        #Place the request via tor
        address = "http://" + os_node['onion_address'] + "/onion_pages/" + os_node['onion_page'] + "/index.html"

        try:
            # #If first make a get
            # #if(driver.current_url + '==' + address):
            # if(i > 0):
            #     logging.debug("Repeating request with refresh()")
            #     driver.refresh()
            # #If same url refresh full page
            # else:
            #     logging.debug("First request with get()")
            #     driver.get(address)
            driver.load_url(address, wait_for_page_body=True)
        except Exception as e:
            logging.debug("Request failed...")
            logging.debug(e)

        #Instruct pcap to stop locally
        # time.sleep(0.5)
        # logging.debug("Stopping traffic capture...")
        # RESTCall(client_host_ip, "stopTrafficCapture", client_cap_folder + "," + sample_name)

        #Instruct pcap to stop on the onion service's end
        #RESTCall(os_node['ansible_host'], "stopTrafficCapture", onion_cap_folder + "," + sample_name)
        
        if request_iterations == 1: break
        else:
            #Wait a sec
            time.sleep(time_between_requests)

def parse_inventory():
    inventory_file_name = 'inventory.cfg'
    data_loader = DataLoader()
    inventory = InventoryManager(loader = data_loader, sources=[inventory_file_name])
    inventory.parse_sources()
    
    os_nodes = []
    coordinator_ip = ""
    for host in inventory.get_hosts():
        print("HOST: " + str(host))
        if(host.vars["node_name"] == "job-coordinator"):
            coordinator_ip = host.vars["ansible_host"]
        if('os-' in host.vars["node_name"]):
            tmp = {}
            tmp["node_name"] = host.vars["node_name"]
            print("node_name: " + str(host.vars["node_name"]))
            tmp["onion_page"] = host.vars["onion_page"]
            print("onion_page: " + str(host.vars["onion_page"]))
            tmp["onion_address"] = host.vars["onion_address"]
            print("onion_address: " + str(host.vars["onion_address"]))
            tmp["onion_popularity"] = host.vars["onion_popularity"]
            print("onion_popularity: " + str(host.vars["onion_popularity"]))
            tmp["ansible_host"] = host.vars["ansible_host"]
            print("ansible_host: " + str(host.vars["ansible_host"]))
            os_nodes.append(tmp)

    return os_nodes, coordinator_ip

def get_node_random(nodes):
    
    if len(nodes) == 1: return nodes[0]

    return_node = None

    while return_node == None:
        sorted_nodes = sorted(nodes, key=lambda node: node['onion_popularity'])
        my_random = random.randint(0, 10000)
        cumulative_sum = 0
        for i in sorted_nodes:
            cumulative_sum += i['onion_popularity']*10000
            if my_random < cumulative_sum:
                return_node = i
                break
        
        if return_node == None:
            print('My_random:', my_random)
            print('Cumulative_sum:', cumulative_sum)
            # TODO: when this situation happens, the script stops, should we choose
            # a random one or just move to the next iteration? because this could distort the results???

    return return_node

if __name__ == '__main__':
    request_iterations = int(sys.argv[1])
    session_iterations = int(sys.argv[2])
    client_host_ip = sys.argv[3]

    onion_services, coordinator_ip = parse_inventory()
    hostname = socket.gethostname()
    print(hostname)

    #Create directory for holding pcaps
    client_cap_folder = home_folder+"pcap-folder/captures-" + hostname + "/"

    #start virtual display for Tor browser
    xvfb_display = start_xvfb()

    #ensure Tor is not running
    os.system('pkill -15 -f /usr/bin/tor')
    os.system('pkill -15 -f /etc/tor/torrc')
    
    time.sleep(random.uniform(0,5))
    times_string = RESTCall(coordinator_ip, "client").text
    startTime = float(times_string.split()[0])
    endTime = float(times_string.split()[1])

    #start browser and Tor
    logging.debug("Starting new Tor system process")
    os.system("/usr/bin/tor -f /etc/tor/torrc &")
    time.sleep(1)
    
    while time.mktime(time.gmtime()) < startTime:
        time.sleep(1)

    i = 0
    while time.mktime(time.gmtime()) < endTime:

        time.sleep(random.uniform(2.0,4.0))
        #Restart browser and Tor for each browsing session
        #Start new capture before restarting Tor and Broswer

        print("========== SESSION ITERATION ==========")
        os_node = get_node_random(onion_services)
        print("===== ONION: hostname: " + hostname + " ; os_node['node_name']: " +  os_node['node_name'] + " ; os_node['onion_page']: " + os_node['onion_page'] +  " ; i:  " + str(i))
        session_sample_name = hostname + "_" + os_node['node_name'] + "_" + os_node['onion_page'] + "_session_" + str(i)
        logging.debug("Session onion: " + os_node['node_name'])

        logging.debug("Starting new Tor Browser Selenium")
        driver = TorBrowserDriver(pathToTorBrowser, tbb_logfile_path="headless_tor_browser.log")
        driver.set_page_load_timeout(30)
        
        #perform browsing session 
        place_request_via_tor(driver, os_node, request_iterations, session_sample_name)
        print("**** place request to tor OS: " + str(os_node))

        print("AFTER lsof")
        #stop Tor Browser and Tor process
        driver.quit()
        print("AFTER driver.quit()")

        i += 1

    os.system('pkill -15 -f /usr/bin/tor')
    os.system('pkill -15 -f /etc/tor/torrc')
    print("after pkill")

    #stop virtual display for Tor Browser
    stop_xvfb(xvfb_display)
    print("AFTER stop_xvfb")

    RESTCall(coordinator_ip, "client_terminate")
    print("AFTER signal_termination")