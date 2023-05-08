import os
import re
import pandas

def main():

    frames_joint = []
    frames_fetch = []
    frames_reply = []

    dir = ''
    kernel = dir.split('/')[-2]
    directory = os.listdir(dir)
    directory.sort()
    for file in directory:
        if re.search('csv',file) == None: continue
        elif re.search('top20s',file) != None: continue
        else:
            mode = file.split('_')[0]
            n_probes = int(file.split('_')[1].split('probes')[0])
            scaling = 'NO' if file.split('_')[2] == 'no' else 'YES'

            df = pandas.read_csv(dir+file)
            df.sort_values(by=['validation_accuracy_%','test_accuracy_%'], inplace=True, ascending=False)
            top20 = df[:20]
            top20.insert(0, 'nr_probes',[n_probes for i in range(20)], allow_duplicates=True)
            top20.insert(2, 'scaling',[scaling for i in range(20)], allow_duplicates=True)

            if mode == 'joint':
                frames_joint.append(top20)
            elif mode == 'fetch':
                frames_fetch.append(top20)
            elif mode == 'reply':
                frames_reply.append(top20)
            

    result_joint = pandas.concat(frames_joint)
    result_fetch = pandas.concat(frames_fetch)
    result_reply = pandas.concat(frames_reply)
    result_joint.sort_values(by=['validation_accuracy_%','test_accuracy_%'], inplace=True, ascending=False)
    result_fetch.sort_values(by=['validation_accuracy_%','test_accuracy_%'], inplace=True, ascending=False)
    result_reply.sort_values(by=['validation_accuracy_%','test_accuracy_%'], inplace=True, ascending=False)
    
    for mode in ['joint', 'fetch', 'reply']:
        with open(dir+mode+'_'+kernel+'_top20s.csv', 'w') as of:
            if mode == 'joint':
                result_joint.to_csv(of)
            elif mode == 'fetch':
                result_fetch.to_csv(of)
            elif mode == 'reply':
                result_reply.to_csv(of)
            of.close()
        with open(dir+kernel+'_top20s.md', 'a') as of:
            of.write(f'# {mode}:\n')
            if mode == 'joint':
                result_joint.to_markdown(of)
            elif mode == 'fetch':
                result_fetch.to_markdown(of)
            elif mode == 'reply':
                result_reply.to_markdown(of)
            of.write('\n')
            of.close()

    return

if __name__ == '__main__':
    main()