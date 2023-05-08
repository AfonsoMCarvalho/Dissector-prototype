import argparse
import os
import pickle
import re

import numpy as np

def main():

    directory = os.listdir(dir)
    for file in directory:
        if re.search('\.pickle',file) == None: continue
        if re.search('separated',file) == None: continue

        fin = open(dir+'/'+file,'rb')
        f_data = pickle.load(fin)
        fin.close()

        data = getMostPopular(f_data)
        l1 = file.split('separated')
        l2 = l1[0].split('_s')
        filename = l2[0] + '_isolated_s' + l2[1] + l1[1][1:]

        fout = open(out+'/'+filename,'wb')
        pickle.dump(data, fout)
        fout.close()

    return

def getMostPopular(data):
    most_bytes = 0
    most_ip = ''
    most_port = ''

    for ip in data.keys():
        for port in data[ip].keys():
            total = sum(data[ip][port][1])
            if total > most_bytes or most_bytes == 0:
                most_bytes = total
                most_ip = ip
                most_port = port

    output = []
    output.append(data[most_ip][most_port][0])
    output.append(data[most_ip][most_port][1])
     
    return output       

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, default=None, help='The directory where the files are (default: %(default)s)')
    parser.add_argument('out', type=str, default=None, help='The directory where the output will be stored (default: %(default)s)')

    args = parser.parse_args()
    dir = args.dir
    out = args.out

    main()