import os

for k in [False]:#, True]: # no_scaling
    for i in ['joint','fetch','reply']: # mode
        for j in [1,2,4,8,12]: # probes
            os.system(f'python3 anomaly_detection.py Mega_w_timeouts/stats/{i}/{i}_train_set.csv Mega_w_timeouts/stats/{i}/{i}_{j}probes_test_set.csv Mega_w_timeouts/stats/anomaly_detection/rbf/{i}_{j}probes.csv Mega_w_timeouts/stats/anomaly_detection/rbf/{i}{"_no_scaling.md" if k else "_scaling.md"} {"-ns" if k else ""}')
