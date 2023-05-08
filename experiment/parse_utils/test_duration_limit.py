import argparse
import os
import pickle
import re
import get_first_last_ts as gflt
import numpy as np

def getSNumber(e):
    if phase == 'merged':
        return int(e.split('session')[1].split('_')[0])
    else:
        return int(e.split('_s')[1].split('_')[0])

def test_length():
    if phase not in ['separated', 'merged']:
        print('ERROR: invalid phase')
        return

    directory = os.listdir(dir)
    count= 0
    directory.sort(key=getSNumber)
    diffs=[]
    for file in directory:
        if re.search('fetch', file) == None: continue
        times = gflt.getJointTs(dir+'/'+file)
        diff = times[1]-times[0]
        diffs.append(diff)
        if diff > limit:
            print(f'{file}: {diff}')
            count+=1
    print(f'\nMEDIAN: {np.median(diffs)}s\nMEAN: {np.mean(diffs)}s\nMAX: {np.max(diffs)}s\nMIN: {np.min(diffs)}s\nCOUNT = {count}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, default=None, help='The directory where the pickle files are (default: %(default)s)')
    parser.add_argument('-phase', type=str, default='merged', help='Either \'separated\' or \'merged\' (default: %(default)s)')
    parser.add_argument('limit', type=int, default=None, help='The limit for the duration of the capture (default: %(default)s)')

    args = parser.parse_args()

    dir = args.dir
    phase = args.phase
    limit = args.limit

    test_length()
