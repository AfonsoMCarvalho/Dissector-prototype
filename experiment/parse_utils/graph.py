import argparse
import os
import pickle
import re
from matplotlib import pyplot as plt

def main():

    data_to_plot = []

    directory = os.listdir(dir)
    for file in directory:
        if re.search('\.pickle', file) == None: continue

        fin = open(dir+'/'+file, 'rb')
        print(file)
        data = pickle.load(fin) 
        fin.close()

        if isinstance(data, dict):
            data = getMostPopular(data)
            data['filename'] = file
        elif isinstance(data, list):
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
            print('ERROR: Data must be either a list or a dictionary')
            continue
        
        if cumulative:
            data = getCumulative(data)

        data_to_plot.append(data)

    if bucket_size != None:
        buckets_start = getBucketsStart(data_to_plot)
        for data in data_to_plot:
            data = putInBuckets(data, buckets_start, bucket_size, cumulative)

    plotGraph(data_to_plot)

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

    output = {}
    output['ip'] = most_ip
    output['port'] = str(most_port)
    output['times'] = data[most_ip][most_port][0]
    output['sizes'] = data[most_ip][most_port][1]
     
    return output


def getCumulative(data):
    cumul = [data['sizes'][0]]

    n_packets = len(data['sizes'])
    for i in range(1, n_packets):
        cumul.append(cumul[i-1]+data['sizes'][i])
    
    data['sizes'] = cumul

    return data

def getBucketsStart(data):
    min = 0
    for dic in data:
        if dic['times'][0] < min or min == 0:
            min = dic['times'][0]

    return min

def putInBuckets(data, buckets_start, bucket_size, cumulative):

    bucket_total = 0
    bucket_end = buckets_start + bucket_size
    sizes = [0]
    times = [buckets_start]

    n_packets = len(data['times'])
    i = 0
    while i < n_packets:
        if data['times'][i] < bucket_end:
            if cumulative:
                bucket_total = data['sizes'][i]
            else:
                bucket_total += data['sizes'][i]
            i += 1
        else:
            sizes.append(bucket_total)
            times.append(bucket_end)
            bucket_end += bucket_size
            if not cumulative:
                bucket_total = 0
    sizes.append(bucket_total)
    times.append(bucket_end)

    data['times'] = times
    data['sizes'] = sizes

    return data

def plotGraph(data):

    if cumulative and bucket_size != None:
        title = 'Bytes transmitted, cumulative. Bucket size = '+str(bucket_size)+'s'
    elif bucket_size != None:
        title = 'Bucket size = '+str(bucket_size)+'s'
    elif cumulative:
        title = 'Bytes transmitted, cumulative'
    else:
        title = 'Bytes transmitted'

    xlabel = 'Time (s)'
    ylabel = 'Packet size (B)'

    fig, ax = plt.subplots(figsize=(9,6))

    origin = None
    for dic in data:
        if origin == None or dic['times'][0] < origin:
            origin = dic['times'][0]

    for dic in data:
        for i in range(len(dic['times'])):
            dic['times'][i] -= origin
        ax.plot(dic['times'],dic['sizes'],label=dic['filename'])

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    #ax.set_title(title)

    plt.xlim(left=0)
    plt.ylim(bottom=0)

    # Sorting the legend
    handles, labels = ax.get_legend_handles_labels()
    sorted_legend = sorted(zip(labels,handles))
    labels = [x for x,_ in sorted_legend]
    handles = [x for _,x in sorted_legend]

    ax.legend(handles=handles, labels=labels)
    plt.savefig('/home/afonso/Documents/the_different_streams.pdf',format='pdf')
    plt.show()

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, default=None, help='The directory where the .pickle files are (default: %(default)s)')
    parser.add_argument('-b', type=float, default=None, nargs=1, help='The size of the buckets (default: %(default)s)')
    parser.add_argument('-c', action='store_true', help='Whether you wish to plot cumulative graphs (default: %(default)s)')

    args = parser.parse_args()
    dir = args.dir
    bucket_size = args.b
    cumulative = args.c

    if bucket_size != None:
        bucket_size = bucket_size[0]

    main()
