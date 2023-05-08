import argparse
import pickle
import re

from h11 import Data

def main():
    if re.search('\.pickle',file) == None:
        print('ERROR: File must be .pickle. ABORTING')
        return

    fin = open(file,'rb')
    data = pickle.load(fin)
    fin.close()

    print(data)
    
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, default=None, help='The file to be cut (default: %(default)s)')

    args = parser.parse_args()
    file = args.file

    main()