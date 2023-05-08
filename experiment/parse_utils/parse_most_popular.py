from ctypes.wintypes import tagSIZE
import os
import argparse
import re

def main():

    pcap_dirs = getDirList(dir)

    for d in pcap_dirs:
        probe = getPNumber(d)
        parse(d, probe)

    return

def getDirList(dir):

    pcap_folders = []
    path = os.walk(dir)

    i = 0
    for root, directories, files in path:
        if files == [] or re.search('pcap',files[0]) == None: 
            continue
        
        pcap_folders.append(root)

    return pcap_folders

def getPNumber(name):
    l = name.split('probe-new')
    if l[1][0] == '/':
        p_number = 1
    elif l[1][0] == '-':
        l[1] = l[1][1:]
        number = ''
        while l[1][0] in ['0','1','2','3','4','5','6','7','8','9']:
            number += l[1][0]
            l[1] = l[1][1:]
        p_number = int(number)
    else:
        print('ERROR')
        return

    print(p_number)
    return p_number

def parse(dir, probe):

    directory = os.listdir(dir)
    directory.sort(key=sortName)
    n_files = len(directory)
    tags = getTags(n_sessions, n_rounds, n_files)

    i = 0
    for file in directory:
        print(dir+'/'+file)
        os.system('python3 parse_pcaps.py -file '+dir+'/'+file+' -t '+str(probe)+'_s'+str(tags[i])+'_separated -s -out '+out)

        i += 1

    return

def sortName(e):
    return int(e.split('_')[-2])

def getTags(n_s, n_r, l):
    tags = []

    spr = l // n_r 
    ipr = n_s - spr + 1
    consec = spr - 1

    i = ipr
    c1 = 0
    c2 = 0
    while c1 < l:
        tags.append(i)
        if c2 < consec:
            i += 1
            c2 += 1
        else:
            i += ipr
            c2 = 0
        c1 += 1

    return tags 

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, default=None, help='The root directory where all the .pcap files are (default: %(default)s)')
    parser.add_argument('-s', type=int, default=4, help='The number of probing sessions per experiment (default: %(default)s)')
    parser.add_argument('-r', type=int, default=50, help='The number of experiment rounds (default: %(default)s)')
    parser.add_argument('out', type=str, default=None, help='The directory where the output will be stored (default: %(default)s)')

    args = parser.parse_args()
    dir = args.dir
    n_sessions = args.s
    n_rounds = args.r
    out = args.out

    main()