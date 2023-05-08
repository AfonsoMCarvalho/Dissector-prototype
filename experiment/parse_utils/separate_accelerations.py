import argparse
import os
import pickle
import re

import matplotlib
import get_first_last_ts as gflt
from matplotlib import pyplot as plt

def separate(file, cut, s_dir, out, pattern=None):
    phase = None
    if re.search('.pickle',file) == None: 
        print('File not pickle. ABORT')
        return

    if "fetch" in file.split('_')[-1]: phase = 'fetch'
    if "reply" in file.split('_')[-1]: phase = 'reply'
    if "joint" in file.split('_')[-1]: phase = 'joint'

    if phase == None:
        print('Can\'t get the phase. ABORT')
        return

    fin = open(file,'rb')
    accels = pickle.load(fin)
    fin.close()

    session_ts = []
    directory = os.listdir(s_dir)
    directory.sort(key=getSNumber)
    if phase == 'joint':
        seen = ''
        for f in directory:
            if re.search(seen,f) == None or seen == '':
                session_ts.append(gflt.getJointTs(s_dir+'/'+f))
                seen = f[:-12]
            else: continue
    else:
        for f in directory:
            if re.search(phase,f) == None: continue
            session_ts.append(gflt.getTs(s_dir+'/'+f))

    if pattern != None:
        i = 0
        for j in session_ts:
            if i == len(pattern):
                i = 0
            j.append(pattern[i])
            i += 1                

    # print(len(session_ts))
    sessions = iter(session_ts)
    size = len(accels[0])
    sample = [[],[]]
    clients_only = []
    during_sessions = []


    current_session = next(sessions)
    start = current_session[0]
    limit = start + cut*60
    if current_session[1] > limit:
        end = limit
    else:
        end = current_session[1]

    i = 0
    inside = False
    while i < size:
        time = accels[0][i] 
        if time > end:
            if inside:
                sample.append(current_session[2])
                during_sessions.append(sample)
                sample = [[],[]]
                inside = False
            try:
                current_session = next(sessions)
            except:
                sample[0].append(time)
                sample[1].append(accels[1][i])
                i += 1
                continue
            start = current_session[0]
            limit = start + cut*60
            if current_session[1] > limit:
                end = limit
            else:
                end = current_session[1]
        elif start <= time <= end:
            if not inside:
                if len(sample[0]) != 0:
                    clients_only.append(sample)
                    sample = [[],[]]
                inside = True
            sample[0].append(time)
            sample[1].append(accels[1][i])
            i += 1
        else:
            inside = False
            sample[0].append(time)
            sample[1].append(accels[1][i])
            i += 1
    if inside:
        sample.append(current_session[2])
        during_sessions.append(sample)
    else:
        clients_only.append(sample)
    
    #print([i[2] for i in during_sessions])
    fout = open(out+'.pickle','wb')
    pickle.dump([clients_only,during_sessions],fout)
    fout.close()

    print(len(clients_only))
    print(len(during_sessions))
    return clients_only, during_sessions

def getSNumber(e):
    return int(e.split('session')[1].split('_')[0])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, default=None, help='The file containing the acceleration data (default: %(default)s)')
    parser.add_argument('-c', type=float, default=3.0, help='The cutoff for the improper sessions in minutes (default: %(default)s)')    
    parser.add_argument('sdir', type=str, default=None, help='The directory where the session files are (default: %(default)s)')
    parser.add_argument('out', type=str, default=None, help='The output file (default: %(default)s)')
    parser.add_argument('-p', nargs='+', type=int, default=None, help='The output file (default: %(default)s)')


    args = parser.parse_args()
    file = args.file
    cut = args.c
    s_dir = args.sdir
    out = args.out
    pattern = args.p

    separate(file, cut, s_dir, out, pattern)