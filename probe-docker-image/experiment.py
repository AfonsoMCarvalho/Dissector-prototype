import os, sys
import logging
import time
import socket
import requests
import random
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import start_xvfb, stop_xvfb
from selenium.webdriver.firefox.options import Options as FirefoxOptions


#logging.disable(logging.DEBUG)

logging.basicConfig(level=logging.DEBUG,filename='/logs/experiment.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

home_folder = "/home/afonso_carvalho/"
docker_home_folder = "./"
pathToTorBrowser = '/tor-browser_en-US'

options = FirefoxOptions()
options.headless = True
options.set_preference('browser.cache.disk.enable', False)
options.set_preference('browser.cache.disk_cache_ssl', False)
options.set_preference('browser.cache.memory.enable', False)
options.set_preference('browser.cache.offline.enable', False)
options.set_preference('browser.privatebrowsing.forceMediaMemoryCache', False)
options.set_preference('devtools.cache.disabled', True)
options.set_preference('dom.caches.enabled', False)
options.set_preference('image.cache.size', 0)
options.set_preference('media.cache.size', 0)
options.set_preference('network.buffer.cache.size', 0)
options.set_preference('privacy.clearsitedata.cache.enabled', True)

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

def place_request_via_tor(driver, os_node, request_iterations, session):
    
    #Cycle request_iterations times through the HS list and place requests
    for i in range(request_iterations):
        logging.debug("Iteration number: %d"%i)
        print("Request number: %d"%i)

        #Place the request via tor
        address = "http://" + os_node['onion_address'] + "/onion_pages/" + os_node['onion_page'] + "/index.html"

        try:
            # #If first make a get
            # #if(driver.current_url + '==' + address):
            # if(session > 0 or i > 0):
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
        
        # if request_iterations == 1: break
        # else:
        #     #Wait a sec
        #     time.sleep(time_between_requests)
    
    return

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

    #start browser and Tor
    logging.debug("Starting new Tor system process")
    os.system("/usr/bin/tor &")
    time.sleep(1)
    
    logging.debug("Starting new Tor Browser Selenium")
    driver = TorBrowserDriver(pathToTorBrowser, tbb_logfile_path="headless_tor_browser.log",options=options)
    driver.set_page_load_timeout(30)

    #driver.get('https://www.google.com')
    
    times_string = RESTCall(coordinator_ip, "probe").text
    startTime = float(times_string.split('_')[0])
    endTime = float(times_string.split('_')[1])
    period = times_string.split('_')[2].strip('][').split(', ')
    rounds = int(times_string.split('_')[3])
    print(period)

    i = 0
    p = 0
    r = 0
    while time.mktime(time.gmtime()) < endTime:
        while time.mktime(time.gmtime()) < startTime:
            time.sleep(1)

        #Start new capture before making the requests

        print("========== SESSION ITERATION ==========")
        os_node = get_node_random(onion_services)
        print("===== ONION: hostname: " + hostname + " ; os_node['node_name']: " +  os_node['node_name'] + " ; os_node['onion_page']: " + os_node['onion_page'] +  " ; i:  " + str(i))
        session_sample_name = hostname + "_" + os_node['node_name'] + "_" + os_node['onion_page'] + "_session_" + str(i)
        logging.debug("Session onion: " + os_node['node_name'])
        print("**** place request to tor OS: " + str(os_node))
        
        RESTCall(client_host_ip, "startTrafficCapture", client_cap_folder + "," + session_sample_name)

        #perform browsing session 
        place_request_via_tor(driver, os_node, request_iterations, i)

        RESTCall(client_host_ip, "stopTrafficCapture", client_cap_folder + "," + session_sample_name)
        

        i += 1

        startTime += float(period[p]) * 60

        p += 1
        if p == len(period):
            p = 0
            r += 1
            if r == rounds:
                break
    
    #stop Tor Browser
    driver.quit()
    print("AFTER driver.quit()")
    #stop Tor process
    os.system('pkill -15 -f /usr/bin/tor')
    os.system('pkill -15 -f /etc/tor/torrc')
    print("after pkill")

    #stop virtual display for Tor Browser
    stop_xvfb(xvfb_display)
    print("AFTER stop_xvfb")

    RESTCall(coordinator_ip, "probe_terminate")
    print("AFTER signal_termination")