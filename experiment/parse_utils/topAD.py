import json
import pprint
import pandas as pd

best = {'reply': {},
        'fetch': {},
        'joint': {}}

for i in ['reply','fetch','joint']:
    for j in [1,2,4,8,12]:
        best_f1 = None
        best_row = []
        for k in ['scaling','no_scaling']:
            df = pd.read_csv(f'Mega_w_timeouts/stats/anomaly_detection/rbf/{i}_{j}probes_{k}_rbf.csv')
            df = df.reset_index()

            for index, row in df.iterrows():
                #if row['gamma'] == 'auto':continue
                recall = row['test_accuracy_%'] / 100
                tp = row['test_accuracy_%'] / 2 # *50/100
                fn = 50 - tp
                tn = row['validation_accuracy_%'] / 4 # *25/100
                fp = 25 - tn
                precision = tp / (tp + fp)
                #f1 = 2 * ((precision * recall)/(precision + recall))
                f1 = (4 * tp * tn)/(4 * tp * tn + (tp + tn)*(fp + fn))
                if best_f1 == None or f1 > best_f1:
                    best_f1 = f1
                    best_row = [(row,k,100-row['validation_accuracy_%'],best_f1)]
                elif f1 == best_f1:
                    best_row.append((row,k,100-row['validation_accuracy_%'],best_f1))

        # if len(best_row) > 1:
        #     print('SEVERAL BEST FOR ')
        #     print(best_row)

        if i == 'reply':
            best['reply'][j] = best_row#,k,100-best_row['validation_accuracy_%']]
        elif i == 'fetch':
            best['fetch'][j] = best_row#,k,100-best_row['validation_accuracy_%']]
        elif i == 'joint':
            best['joint'][j] = best_row#,k,100-best_row['validation_accuracy_%']]

for dic in best.keys():
    for probes in best[dic].keys():
        print(f'{dic}-{probes} probes:({len(best[dic][probes])})\n{best[dic][probes]}\n')
                