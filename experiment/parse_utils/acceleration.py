import argparse
import os
import pickle
import re

import matplotlib
import get_first_last_ts
from matplotlib import pyplot as plt

def main():

    data_to_plot = []
    phase = ''
    if re.search('\.pickle', file) == None: return
    if "fetch" in file.split('_'): phase = 'fetch'
    if "reply" in file.split('_'): phase = 'reply'
    fin = open(file, 'rb')
    print(file)
    data = pickle.load(fin)
    fin.close()

    if isinstance(data, list):
        ip = 'Any'
        port = 'Any'
        times = data[0]
        sizes = data[1]

        data = {}
        data['ip'] = ip
        data['port'] = port
        data['times'] = times
        data['sizes'] = sizes
        data['filename'] = file

    else:
        print('ERROR: Data must be a list')
        return

    data_to_plot.append(data)

    buckets_start = getBucketsStart(data_to_plot)
    #for data in data_to_plot:
        #data = putInBuckets(data, buckets_start, bucket_size)
        #data = calcSpeed(data, bucket_size)
        #data = calcAccel(data, bucket_size)

    if export != None:
        fout = open(export+'.pickle','wb')
        pickle.dump([data['times'],data['sizes']],fout)
        fout.close()
        print('Saved data in '+export+'.pickle')
        return 

    if s_dir != None:
        sessions = []
        directory = os.listdir(s_dir)
        for f in directory:
            if re.search('session',f) == None: continue
            assert phase != ''
            if re.search(phase, f) == None: continue
            session = {}
            for s in f.split('_'):
                if re.search('session',s) != None:
                    session['name'] = s
            
            times = get_first_last_ts.getTs(s_dir+'/'+f)

            session['start'] = times[0]
            session['end'] = times[1]

            sessions.append(session)
    else:
        sessions = None

    plotGraph(data_to_plot, sessions)

    return

def plotGraph(data, sessions):

    title = 'Acceleration of bytes transmitted. Bucket size = '+str(bucket_size)+'s'
    xlabel = 'Time (s)'
    #ylabel = 'Acceleration (MB/$s^2$)'
    #ylabel = 'Throughput (MB/s)'
    ylabel = 'Packet size (KB)'

    fig, ax = plt.subplots(figsize=(12,6))

    colors = iter(matplotlib.rcParams['axes.prop_cycle'].by_key()['color'])

    origin = None
    for dic in data:
        if origin == None or dic['times'][0] < origin:
            origin = dic['times'][0]

    for dic in data:
        for i in range(len(dic['times'])):
            dic['times'][i] -= origin
            dic['sizes'][i] /= 1000
        c = next(colors)
        #ax.plot(dic['times'],dic['sizes'],label=dic['filename'].split('/')[-1], color = c)
        ax.plot(dic['times'],dic['sizes'],label='Reply packet sizes',color=c)
    if sessions != None:
        for session in sessions:
            try:
                c = next(colors)
            except:
                colors = iter(matplotlib.rcParams['axes.prop_cycle'].by_key()['color'])
                c = next(colors)
            #ax.axvline(session['start'],label=session['name'], color = c)
            ax.axvline(session['start']-origin,label='Probing session limits', color = c)
            ax.axvline(session['end']-origin, color = c)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    #ax.set_title(title)
    
    #plt.ticklabel_format(axis='y',style='sci',scilimits=(0,0))
    plt.subplots_adjust(top=0.975,bottom=0.080,right=0.975,left=0.050)#left=0.125)
    plt.xlim(left=0)
    plt.ylim(bottom=0,top=25)

    # Sorting the legend
    handles, labels = ax.get_legend_handles_labels()
    # sorted_legend = sorted(zip(labels,handles))
    # labels = [x for x,_ in sorted_legend]
    # handles = [x for _,x in sorted_legend]

    ax.legend(handles=handles, labels=labels)

    plt.savefig('/home/afonso/Documents/packet_sizes_raw_v2.pdf',format='pdf')
    plt.show()

    return

def calcAccel(data, bucket_size):
    n_sizes = len(data['sizes'])

    temp = [data['sizes'][0]]
    for i in range(1,n_sizes):
        temp.append(data['sizes'][i]-data['sizes'][i-1])
    data['sizes'] = temp

    n_packets = len(data['packets']) #should be the same but still...

    temp = [data['packets'][0]]
    for i in range(1,n_packets):
        temp.append(data['packets'][i]-data['packets'][i-1])
    data['packets'] = temp

    data['sizes'] = [(i/bucket_size) for i in data['sizes']]
    data['packets'] = [(i/bucket_size) for i in data['packets']]

    return data

def calcSpeed(data, bucket_size):
    data['sizes'] = [(i/bucket_size) for i in data['sizes']]
    data['packets'] = [(i/bucket_size) for i in data['packets']]
    return data

def putInBuckets(data, buckets_start, bucket_size):

    bucket_total_bytes = 0
    bucket_total_packets = 0
    bucket_end = buckets_start + bucket_size
    sizes = [0]
    packets = [0]
    times = [buckets_start]

    n_packets = len(data['times'])
    i = 0
    while i < n_packets:
        if data['times'][i] < bucket_end:
            bucket_total_bytes += data['sizes'][i]
            bucket_total_packets += 1
            i += 1
        else:
            sizes.append(bucket_total_bytes)
            times.append(bucket_end)
            packets.append(bucket_total_packets)
            bucket_end += bucket_size
            bucket_total_bytes = 0
            bucket_total_packets = 0

    sizes.append(bucket_total_bytes)
    times.append(bucket_end)
    packets.append(bucket_total_packets)

    data['times'] = times
    data['sizes'] = sizes
    data['packets'] = packets

    return data

def getBucketsStart(data):
    min = 0
    for dic in data:
        if dic['times'][0] < min or min == 0:
            min = dic['times'][0]

    return min

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, default=None, help='The file to be cut (default: %(default)s)')
    # parser.add_argument('dir', type=str, default=None, help='The directory where the .pickle files are (default: %(default)s)')
    parser.add_argument('b', type=float, default=None, nargs=1, help='The size of the buckets in seconds (default: %(default)s)')    
    parser.add_argument('-sdir', type=str, default=None, help='The directory where the session files are (default: %(default)s)')
    parser.add_argument('-export', type=str, default=None, help='Skip generating the graph and save acceleration data to a file (default: %(default)s)')

    args = parser.parse_args()
    # dir = args.dir
    file = args.file
    bucket_size = args.b
    s_dir = args.sdir
    export = args.export

    if bucket_size != None: bucket_size = bucket_size[0]

    main()
