import argparse
from fileinput import filename
from ipaddress import ip_interface
import os
import pickle
import re
import socket
from struct import pack
import sys
import dpkt

def main(file, dir, ip, out_dir, separate, tag):

    roles = {'client': False,
             'onion': False,
             'probe': False}

    outputs = {}
    if separate:
        outputs['fetch'] = {}
        outputs['reply'] = {}
    else:
        outputs['fetch'] = [[],[]]
        outputs['reply'] = [[],[]]

    if file != None:
        outputs, roles = parsePcap(file, ip, outputs, roles)
    else:
        directory = os.listdir(dir)
        directory.sort()
        for file in directory:
            outputs, roles = parsePcap(dir+'/'+file, ip, outputs, roles)

    if out_dir == None:
        if dir == None:
            save_dir = ''
            for s in file.split('/')[:-1]:
                save_dir += s + '/'
        else: save_dir = dir
    else: save_dir = out_dir

    saveResults(outputs, save_dir, tag, roles)

    return

def parsePcap(file, ip, outputs, roles):

    if re.search('\.pcap',file) == None: return outputs, roles

    if re.search("client\.pcap",file) != None: roles['client'] = True
    elif re.search("hs\.pcap",file) != None: roles['onion'] = True
    elif re.search("probe\.pcap",file) != None: roles['probe'] = True
    else: return outputs, roles

    fin = open(file,'rb')    
    print(file)
    pcap = dpkt.pcap.Reader(fin)

    packetTimesIn = []
    packetTimesOut = []
    packetSizesIn = []
    packetSizesOut = []

    ###################################
    # Diogo's Features Here
    ###################################

    # Analyse packets transmited
    totalPackets = 0
    totalPacketsIn = 0
    totalPacketsOut = 0

    # Analyse bytes transmitted
    totalBytes = 0
    totalBytesIn = 0
    totalBytesOut = 0

    ###################################################################
    # Workaround to deal with packet captures that are severed 
    # in the middle of a packet. We read packets one by one using 
    # the pcap's iterator directly. We then deal with possibly broken
    # packets at the end of the capture within the 'for' loop. 
    # This avoids full captures to be thrown away due to a spurious 
    # corrupted packet.
    ###################################################################

    #Read one by one
    packets = []
    i = 0
    while True:
        try:
            ts, buf = pcap.__next__()
            packets.append([ts,buf])
            i += 1
        except Exception as e:
            #Break when we find a corrupted packet at the end of the capture
            #print("Stopped in packet %d from %s"%(i, sample))
            break
    
    fin.close()

    #Process packets (skip seldomly corrupted ones)
    for ts, buf in packets:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                continue

            ip_hdr = eth.data

            # Target TCP communication
            if (ip_hdr.p == 6):
                src_ip_addr_str = socket.inet_ntoa(ip_hdr.src)
                dst_ip_addr_str = socket.inet_ntoa(ip_hdr.dst)
                tcp = ip_hdr.data

                #Do not target packets produced due to synchronizing REST calls
                if(tcp.dport == 5005 or tcp.sport == 5005):
                    continue

                #Do not target packets produced due to ssh
                elif(tcp.dport == 22 or tcp.sport == 22):
                    continue 
                
                elif(len(tcp.data) == 0):
                    continue

                # If machine is recipient (OS)
                if(dst_ip_addr_str == ip and roles['onion']): # Onion receiving fetch
                    if separate:
                        if src_ip_addr_str not in outputs['fetch'].keys():
                            outputs['fetch'][src_ip_addr_str] = {}
                            outputs['fetch'][src_ip_addr_str][tcp.sport] = [[],[]]
                        elif tcp.sport not in outputs['fetch'][src_ip_addr_str].keys():
                            outputs['fetch'][src_ip_addr_str][tcp.sport] = [[],[]]

                        outputs['fetch'][src_ip_addr_str][tcp.sport][0].append(ts)
                        outputs['fetch'][src_ip_addr_str][tcp.sport][1].append(len(buf))
                        
                    else:
                        outputs['fetch'][0].append(ts)
                        outputs['fetch'][1].append(len(buf))

                elif(dst_ip_addr_str == ip and (roles['client'] or roles['probe'])): # Client/Probe receiving reply
                    if separate:
                        if src_ip_addr_str not in outputs['reply'].keys():
                            outputs['reply'][src_ip_addr_str] = {}
                            outputs['reply'][src_ip_addr_str][tcp.sport] = [[],[]]
                        elif tcp.sport not in outputs['reply'][src_ip_addr_str].keys():
                            outputs['reply'][src_ip_addr_str][tcp.sport] = [[],[]]

                        outputs['reply'][src_ip_addr_str][tcp.sport][0].append(ts)
                        outputs['reply'][src_ip_addr_str][tcp.sport][1].append(len(buf))
                        
                    else:
                        outputs['reply'][0].append(ts)
                        outputs['reply'][1].append(len(buf))

                # If machine is sender
                elif(src_ip_addr_str == ip and roles['onion']): # Onion sending reply
                    if separate:
                        if dst_ip_addr_str not in outputs['reply'].keys():
                            outputs['reply'][dst_ip_addr_str] = {}
                            outputs['reply'][dst_ip_addr_str][tcp.dport] = [[],[]]
                        elif tcp.dport not in outputs['reply'][dst_ip_addr_str].keys():
                            outputs['reply'][dst_ip_addr_str][tcp.dport] = [[],[]]

                        outputs['reply'][dst_ip_addr_str][tcp.dport][0].append(ts)
                        outputs['reply'][dst_ip_addr_str][tcp.dport][1].append(len(buf))
                        
                    else:
                        outputs['reply'][0].append(ts)
                        outputs['reply'][1].append(len(buf))

                elif(src_ip_addr_str == ip and (roles['client'] or roles['probe'])): # Client/Probe sending fetch
                    if separate:
                        if dst_ip_addr_str not in outputs['fetch'].keys():
                            outputs['fetch'][dst_ip_addr_str] = {}
                            outputs['fetch'][dst_ip_addr_str][tcp.dport] = [[],[]]
                        elif tcp.dport not in outputs['fetch'][dst_ip_addr_str].keys():
                            outputs['fetch'][dst_ip_addr_str][tcp.dport] = [[],[]]

                        outputs['fetch'][dst_ip_addr_str][tcp.dport][0].append(ts)
                        outputs['fetch'][dst_ip_addr_str][tcp.dport][1].append(len(buf))
                        
                    else:
                        outputs['fetch'][0].append(ts)
                        outputs['fetch'][1].append(len(buf))

                else: continue                

                # Bytes transmitted statistics
                if (src_ip_addr_str == ip):
                    totalBytesOut += len(buf)
                    totalPacketsOut += 1
                elif(dst_ip_addr_str == ip):
                    totalBytesIn += len(buf)
                    totalPacketsIn += 1
                
        except Exception as e:
            #print(e) #Uncomment to check what error is showing up when reading the pcap
            #Skip this corrupted packet
            continue

    return outputs, roles

def saveResults(outputs, save_dir, tag, roles):

    if roles['client']:
        filename = 'client'
    elif roles['probe']:
        filename = 'probe'
    elif roles['onion']:
        filename = 'hs'
    else: 
        print('ERROR detecting the role')
        return

    filename += '_'+tag

    f_fout = open(save_dir+filename+'_fetch.pickle', 'wb')
    r_fout = open(save_dir+filename+'_reply.pickle', 'wb')
    pickle.dump(outputs['fetch'], f_fout)
    pickle.dump(outputs['reply'], r_fout)
    f_fout.close()
    r_fout.close()
    
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', type=str, default=None, help='The directory where the .pcap files to be parsed are (default: %(default)s)')
    parser.add_argument('-file', type=str, default=None, help='The .pcap to be parsed (default: %(default)s)')
    parser.add_argument('-ip', type=str, default='172.17.0.2', help='The ip of the docker container (default: %(default)s)')
    parser.add_argument('-out', type=str, default=None, help='The directory where the output will be stored (default: Same as .pcap files)')
    parser.add_argument('-s', action='store_true', help='Whether you wish to sepearate all IP/PORT pairs (default: %(default)s)')
    parser.add_argument('-t', type=str, default='parsed', help='A tag to be appended to the name of the output file (default: %(default)s)')

    args = parser.parse_args()
    file = args.file
    dir = args.dir
    ip = args.ip
    out_dir = args.out
    separate = args.s
    tag = args.t

    if dir == file == None:
        print('You must specify either a file or a directory. ABORTING')
    elif (dir != None) and (file != None):
        print('You specified both a file and a directory. PARSING FILE: ' + file)
        dir = None
        main(file, dir, ip, out_dir, separate, tag)
    else:
        main(file, dir, ip, out_dir, separate, tag)