import pandas as pd
import argparse
import re
import os
import numpy as np

def main():
    stats_dir = '/'.join(file.split('/')[:-1])
    for i in ['fetch','joint','reply','anomaly_detection']:
        os.system(f'mkdir {stats_dir}/{i}')

    original = pd.read_csv(file)

    # FETCH
    fetch_col_names = []
    for col_name in original.columns:
        if re.search('fetch',col_name) != None:
            fetch_col_names.append(col_name)
    fetch_col_names.extend(['Nr_of_Probes','Class'])

    fetch_df = original.loc[:,fetch_col_names]
    fetch_df.to_csv(stats_dir+'/fetch/fetch_all.csv',index=False)

    # JOINT
    joint_col_names = []
    for col_name in original.columns:
        if re.search('joint',col_name) != None:
            joint_col_names.append(col_name)
    joint_col_names.extend(['Nr_of_Probes','Class'])

    joint_df = original.loc[:,joint_col_names]
    joint_df.to_csv(stats_dir+'/joint/joint_all.csv',index=False)

    # REPLY
    reply_col_names = []
    for col_name in original.columns:
        if re.search('reply',col_name) != None:
            reply_col_names.append(col_name)
    reply_col_names.extend(['Nr_of_Probes','Class'])

    reply_df = original.loc[:,reply_col_names]
    reply_df.to_csv(stats_dir+'/reply/reply_all.csv',index=False)


    # FOR ANOMALY DETECTION
    # TRAINING SETS
    # Fetch
    train_fetch_df = fetch_df.loc[fetch_df['Nr_of_Probes'] == 0]
    train_fetch_df = train_fetch_df.drop('Nr_of_Probes',axis=1)
    train_fetch_df = train_fetch_df.drop('Class',axis=1)
    train_fetch_df.to_csv(f'{stats_dir}/fetch/fetch_train_set.csv',index=False)
    # Joint
    train_joint_df = joint_df.loc[joint_df['Nr_of_Probes'] == 0]
    train_joint_df = train_joint_df.drop('Nr_of_Probes',axis=1)
    train_joint_df = train_joint_df.drop('Class',axis=1)
    train_joint_df.to_csv(f'{stats_dir}/joint/joint_train_set.csv',index=False)
    # Reply
    train_reply_df = reply_df.loc[reply_df['Nr_of_Probes'] == 0]
    train_reply_df = train_reply_df.drop('Nr_of_Probes',axis=1)
    train_reply_df = train_reply_df.drop('Class',axis=1)
    train_reply_df.to_csv(f'{stats_dir}/reply/reply_train_set.csv',index=False)

    # TESTING SETS
    for probe in probes:
        # Fetch
        test_probe_fetch_df = fetch_df.loc[fetch_df['Nr_of_Probes'] == probe]
        test_probe_fetch_df = test_probe_fetch_df.drop('Nr_of_Probes',axis=1)
        test_probe_fetch_df = test_probe_fetch_df.drop('Class',axis=1)
        test_probe_fetch_df.to_csv(f'{stats_dir}/fetch/fetch_{probe}probes_test_set.csv',index=False)
        # Joint
        test_probe_joint_df = joint_df.loc[joint_df['Nr_of_Probes'] == probe]
        test_probe_joint_df = test_probe_joint_df.drop('Nr_of_Probes',axis=1)
        test_probe_joint_df = test_probe_joint_df.drop('Class',axis=1)
        test_probe_joint_df.to_csv(f'{stats_dir}/joint/joint_{probe}probes_test_set.csv',index=False)
        # Reply
        test_probe_reply_df = reply_df.loc[reply_df['Nr_of_Probes'] == probe]
        test_probe_reply_df = test_probe_reply_df.drop('Nr_of_Probes',axis=1)
        test_probe_reply_df = test_probe_reply_df.drop('Class',axis=1)
        test_probe_reply_df.to_csv(f'{stats_dir}/reply/reply_{probe}probes_test_set.csv',index=False)

    # FOR CLASSIFIERS
    for probe in probes:
        # Fetch
        probe_fetch_df = fetch_df.loc[fetch_df['Nr_of_Probes'].isin([0,probe])]
        probe_fetch_df = probe_fetch_df.drop('Nr_of_Probes',axis=1)

        max = findMax(probe_fetch_df['Differential_Entropy_fetch'])
        min = findMin(probe_fetch_df['Differential_Entropy_fetch'])
        probe_fetch_df['Differential_Entropy_fetch'].replace(np.inf, max, inplace=True)
        probe_fetch_df['Differential_Entropy_fetch'].replace(-np.inf, min, inplace=True)

        probe_fetch_df.to_csv(f'{stats_dir}/fetch/classifier_fetch_{probe}probes.csv',index=False)

        # Joint
        probe_joint_df = joint_df.loc[joint_df['Nr_of_Probes'].isin([0,probe])]
        probe_joint_df = probe_joint_df.drop('Nr_of_Probes',axis=1)

        max = findMax(probe_joint_df['Differential_Entropy_joint'])
        min = findMin(probe_joint_df['Differential_Entropy_joint'])
        probe_joint_df['Differential_Entropy_joint'].replace(np.inf, max, inplace=True)
        probe_joint_df['Differential_Entropy_joint'].replace(-np.inf, min, inplace=True)

        probe_joint_df.to_csv(f'{stats_dir}/joint/classifier_joint_{probe}probes.csv',index=False)

        # Reply
        probe_reply_df = reply_df.loc[reply_df['Nr_of_Probes'].isin([0,probe])]
        probe_reply_df = probe_reply_df.drop('Nr_of_Probes',axis=1)

        max = findMax(probe_reply_df['Differential_Entropy_reply'])
        min = findMin(probe_reply_df['Differential_Entropy_reply'])
        probe_reply_df['Differential_Entropy_reply'].replace(np.inf, max, inplace=True)
        probe_reply_df['Differential_Entropy_reply'].replace(-np.inf, min, inplace=True)

        probe_reply_df.to_csv(f'{stats_dir}/reply/classifier_reply_{probe}probes.csv',index=False)

    return

def findMax(vector):
    max = None
    for value in vector:
        if value == np.inf or value == -np.inf: continue
        else:
            if max == None or value > max:
                max = value
    return max

def findMin(vector):
    min = None
    for value in vector:
        if value == np.inf or value == -np.inf: continue
        else:
            if min == None or value < min:
                min = value
    return min

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, default=None, help='The csv file with the entire dataset (default: %(default)s)')
    parser.add_argument('-p', nargs='+', type=int, default=[1,2,4,8,12], help='Sets os probes used (default: %(default)s))')
    args = parser.parse_args()

    file = args.file
    probes = args.p

    main()