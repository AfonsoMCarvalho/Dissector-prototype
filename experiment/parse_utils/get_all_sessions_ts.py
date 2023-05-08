import argparse
import os
import pickle
import re
import get_first_last_ts as gflt

def listTs(dir, exp):
    ts_list_fetch = []
    ts_list_reply = []

    os.system('mv '+dir+'/*_fetch.pickle '+exp)
    directory = os.listdir(exp)
    directory.sort(key=sortNames)
    for file in directory:
        ts_list_fetch.append(gflt.getTs(exp+'/'+file))

    os.system('mv '+exp+'/* '+dir)

    os.system('mv '+dir+'/*_reply.pickle '+exp)
    directory = os.listdir(exp)
    directory.sort(key=sortNames)
    for file in directory:
        ts_list_reply.append(gflt.getTs(exp+'/'+file))

    os.system('mv '+exp+'/* '+dir)

    print(ts_list_fetch)
    print(ts_list_reply)

    return ts_list_fetch, ts_list_reply

def sortNames(e):
    return int(e.split('session')[1].split('_')[0])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, default=None, help='The directory where the session .pickle files are (default: %(default)s)')
    parser.add_argument('exp', type=str, default=None, help='The directory where the script will run (default: %(default)s)')

    args = parser.parse_args()
    dir = args.dir
    exp = args.exp

    listTs(dir, exp)