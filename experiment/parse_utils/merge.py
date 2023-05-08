import argparse
import os
import pickle
import re

import numpy as np

def main():

    data = [[],[]]

    directory = os.listdir(dir)
    directory.sort()
    for file in directory:
        if re.search('\.pickle',file) == None: continue

        fin = open(dir+'/'+file,'rb')
        f_data = pickle.load(fin)
        fin.close()

        data[0].extend(f_data[0])
        data[1].extend(f_data[1])
    
    np_times = np.array(data[0])
    np_sizes = np.array(data[1])

    index = np.argsort(np_times)

    data[0] = np_times[index].tolist()
    data[1] = np_sizes[index].tolist()

    fout = open(dir+'/'+tag+'.pickle','wb')
    pickle.dump(data, fout)
    fout.close()

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, default=None, help='The directory where the files are (default: %(default)s)')
    parser.add_argument('-t', type=str, default='merged', help='A tag to be appended to the output filename (default: %(default)s)')

    args = parser.parse_args()
    dir = args.dir
    tag = args.t

    main()