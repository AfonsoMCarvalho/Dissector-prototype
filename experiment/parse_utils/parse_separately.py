import argparse
import os

def main():

    directory = os.listdir(dir)
    directory.sort()
    n_files = len(directory)
    dif = n_sessions - n_files + 1

    i = 0
    for file in directory:
        print(dir+'/'+file)
        os.system('python3 parse_pcaps.py -file '+dir+'/'+file+' -t '+str(probe)+'_s'+str(i+dif)+' -out '+out)

        i += 1

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, default=None, help='The directory where the files are (default: %(default)s)')
    parser.add_argument('-out', type=str, default=None, help='The directory where the output will be stored (default: Same as .pcap files)')
    parser.add_argument('p', type=int, default=None, help='The probe number (default: %(default)s)')
    parser.add_argument('-s', type=int, default=4, help='The number of probing sessions (default: %(default)s)')
    parser.add_argument('-t', type=str, default=None, help='A tag to be appended to the output filename (default: %(default)s)')

    args = parser.parse_args()
    dir = args.dir
    out = args.out
    probe = args.p
    n_sessions = args.s
    tag = args.t

    if out == None: out = dir

    main()