import argparse
import pickle
import re

def getTs(file):
    if re.search('\.pickle',file) == None:
        print('ERROR: File must be .pickle. ABORTING')
        return

    fin = open(file,'rb')
    data = pickle.load(fin)
    fin.close()

    output = [data[0][0], data[0][-1]]
    #print(output)
    
    return output

def getJointTs(file):

    if re.search('\.pickle',file) == None:
        print('ERROR: File must be .pickle. ABORTING')
        return

    output = []
    f_fetch = ''
    f_reply = ''

    if re.search('fetch',file) != None:
        f_fetch = file
        f_reply = file.split('fetch')[0]+'reply.pickle'

    elif re.search('reply',file) != None:
        f_reply = file
        f_fetch = file.split('reply')[0]+'fetch.pickle'

    else:
        print('ERROR: File must either be "reply" or "fetch". ABORTING')
        return

    fin_fetch = open(f_fetch,'rb')
    data_fetch = pickle.load(fin_fetch)
    fin_fetch.close()

    fin_reply = open(f_reply,'rb')
    data_reply = pickle.load(fin_reply)
    fin_reply.close()

    output = [data_fetch[0][0], data_reply[0][-1]]
    #print(output)
    
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, default=None, help='The file to be analysed (default: %(default)s)')
    parser.add_argument('-j', action='store_true', help='Return the joint TS (default: %(default)s)')

    args = parser.parse_args()
    file = args.file
    joint = args.j

    if joint:
        print(getJointTs(file))
    else:
        print(getTs(file))