import argparse
import pickle


def main():

    if start == end == between == None:
        print('ERROR: Specify where to cut')
        return

    fin = open(file,'rb')
    data = pickle.load(fin)
    fin.close()

    if between != None:
        if between[0] > between[1]:
            print('ERROR: Start must come before End. ABORTING')
            return
        else:
            data = cutBetween(data, between)
    elif start != None and end != None:
        if start > end:
            print('ERROR: Start must come before End. ABORTING')
            return
        else:
            new_between = [start,end]
            data = cutBetween(data, new_between)
    elif start != None:
        data = cutStart(data, start)
    else:
        data = cutEnd(data, end)

    filename = file.split('.pickle')
    filename = filename[0]+'_'+ tag +'.pickle'

    fout = open(filename,'wb')
    pickle.dump(data, fout)
    fout.close()
    return

def cutStart(data, start):

    total = 0

    while data[0][0] < start:
        del data[0][0]
        del data[1][0]
        total += 1

    if data [0][0] != start:
        data[0].insert(0,start)
        data[1].insert(0,0)

    print('Start: Deleted '+str(total)+' packets')
    return data

def cutEnd(data, end):

    total = 0

    while data[0][-1] > end:
        del data[0][-1]
        del data[1][-1]
        total += 1

    if data [0][-1] != end:
        data[0].insert(-1,end)
        data[1].insert(-1,0)

    print('End: Deleted '+str(total)+' packets')
    return data

def cutBetween(data, between):

    data = cutStart(data, between[0])
    data = cutEnd(data, between[1])

    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, default=None, help='The file to be cut (default: %(default)s)')
    parser.add_argument('-s', type=float, nargs=1, default=None, help='Where you want the file to start (default: %(default)s)')
    parser.add_argument('-e', type=float, nargs=1, default=None, help='Where you want the file to end (default: Same as .pcap files)')
    parser.add_argument('-b', type=float, nargs=2, default=None, help='Cut between two time values (default: %(default)s)')
    parser.add_argument('-t', type=str, default='cut', help='A tag to be appended to the output filename (default: %(default)s)')

    args = parser.parse_args()
    file = args.file
    start = args.s
    end = args.e
    between = args.b
    tag = args.t

    if start != None:
        start = start[0]

    if end != None:
        end = end[0]

    if between != None:
        between = between

    main()          