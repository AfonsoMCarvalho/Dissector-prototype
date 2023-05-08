import argparse
import os

def main():

    for i in range(n_sessions):
        os.system('mv '+dir+'*s'+str(i+1)+'_fetch.pickle '+exp)
        os.system('python3 merge.py '+exp+' -t '+tag+'session'+str(i+1)+'_fetch')
        os.system('mv '+exp+'/isolated_session* '+out)
        os.system('mv '+exp+'/* '+dir)

        os.system('mv '+dir+'*s'+str(i+1)+'_reply.pickle '+exp)
        os.system('python3 merge.py '+exp+' -t '+tag+'session'+str(i+1)+'_reply')
        os.system('mv '+exp+'/isolated_session* '+out)
        os.system('mv '+exp+'/* '+dir)

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, default=None, help='The directory where the files are (default: %(default)s)')
    parser.add_argument('exp_dir', type=str, default=None, help='The directory where the merge will occur (default: %(default)s)')
    parser.add_argument('out', type=str, default=None, help='The directory where the output will be saved (default: %(default)s)')
    parser.add_argument('-p', type=int, default=10, help='The number of probes (default: %(default)s)')
    parser.add_argument('-s', type=int, default=4, help='The number of probing sessions per round (default: %(default)s)')
    parser.add_argument('-r', type=int, default=50, help='The number of experiment rounds (default: %(default)s)')
    parser.add_argument('-t', type=str, default='', help='A tag to be appended to the output filename (should end in \'_\') (default: %(default)s)')

    args = parser.parse_args()
    dir = args.dir
    exp = args.exp_dir
    out = args.out
    n_probes = args.p
    n_s = args.s
    n_r = args.r
    tag = args.t

    n_sessions = n_s * n_r

    main()