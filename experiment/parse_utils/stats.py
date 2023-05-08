import copy
import re
import statistics
from matplotlib import pyplot as plt
import matplotlib
import pandas as pd
import separate_accelerations as sa
import scipy.stats as st
import numpy as np
from seaborn import stripplot as splot

def calcStats():
    data = {'Minimum_fetch': [],
            'Maximum_fetch': [],
            'Mean_fetch': [],
            'Variance_fetch': [],
            'Skewness_fetch': [],
            'Kurtosis_fetch': [],
            'Geometric_Mean_fetch': [],
            'Harmonic_Mean_fetch': [],
            'Mode_fetch': [],
            'Mode_Count_fetch': [],
            'Moment_fetch': [],
            'Kth-Stat_n1_fetch': [],
            'Kth-Stat_n2_fetch': [],
            'Kth-Stat_n3_fetch': [],
            'Kth-Stat_n4_fetch': [],
            'Kth-Stat_Variance_n1_fetch': [],
            'Kth-Stat_Variance_n2_fetch': [],
            'Geometric_Standard_Deviation_fetch': [],
            'IQR_25_75_fetch': [],
            'IQR_5_95_fetch': [],
            'Standard_Error_Mean_fetch': [],
            'BCI_Mean_center_fetch': [],
            'BCI_Variance_center_fetch': [],
            'BCI_Standard_Deviation_center_fetch': [],
            'BCI_Mean_upper_bound_fetch': [],
            'BCI_Variance_upper_bound_fetch': [],
            'BCI_Standard_Deviation_upper_bound_fetch': [],
            'BCI_Mean_lower_bound_fetch': [],
            'BCI_Variance_lower_bound_fetch': [],
            'BCI_Standard_Deviation_lower_bound_fetch': [],
            'Differential_Entropy_fetch': [],
            'Median_fetch': [],
            'Median_Absolute_Deviation_fetch': [],
            'Minimum_reply': [],
            'Maximum_reply': [],
            'Mean_reply': [],
            'Variance_reply': [],
            'Skewness_reply': [],
            'Kurtosis_reply': [],
            'Geometric_Mean_reply': [],
            'Harmonic_Mean_reply': [],
            'Mode_reply': [],
            'Mode_Count_reply': [],
            'Moment_reply': [],
            'Kth-Stat_n1_reply': [],
            'Kth-Stat_n2_reply': [],
            'Kth-Stat_n3_reply': [],
            'Kth-Stat_n4_reply': [],
            'Kth-Stat_Variance_n1_reply': [],
            'Kth-Stat_Variance_n2_reply': [],
            'Geometric_Standard_Deviation_reply': [],
            'IQR_25_75_reply': [],
            'IQR_5_95_reply': [],
            'Standard_Error_Mean_reply': [],
            'BCI_Mean_center_reply': [],
            'BCI_Variance_center_reply': [],
            'BCI_Standard_Deviation_center_reply': [],
            'BCI_Mean_upper_bound_reply': [],
            'BCI_Variance_upper_bound_reply': [],
            'BCI_Standard_Deviation_upper_bound_reply': [],
            'BCI_Mean_lower_bound_reply': [],
            'BCI_Variance_lower_bound_reply': [],
            'BCI_Standard_Deviation_lower_bound_reply': [],
            'Differential_Entropy_reply': [],
            'Median_reply': [],
            'Median_Absolute_Deviation_reply': [],
            'Minimum_joint': [],
            'Maximum_joint': [],
            'Mean_joint': [],
            'Variance_joint': [],
            'Skewness_joint': [],
            'Kurtosis_joint': [],
            'Geometric_Mean_joint': [],
            'Harmonic_Mean_joint': [],
            'Mode_joint': [],
            'Mode_Count_joint': [],
            'Moment_joint': [],
            'Kth-Stat_n1_joint': [],
            'Kth-Stat_n2_joint': [],
            'Kth-Stat_n3_joint': [],
            'Kth-Stat_n4_joint': [],
            'Kth-Stat_Variance_n1_joint': [],
            'Kth-Stat_Variance_n2_joint': [],
            'Geometric_Standard_Deviation_joint': [],
            'IQR_25_75_joint': [],
            'IQR_5_95_joint': [],
            'Standard_Error_Mean_joint': [],
            'BCI_Mean_center_joint': [],
            'BCI_Variance_center_joint': [],
            'BCI_Standard_Deviation_center_joint': [],
            'BCI_Mean_upper_bound_joint': [],
            'BCI_Variance_upper_bound_joint': [],
            'BCI_Standard_Deviation_upper_bound_joint': [],
            'BCI_Mean_lower_bound_joint': [],
            'BCI_Variance_lower_bound_joint': [],
            'BCI_Standard_Deviation_lower_bound_joint': [],
            'Differential_Entropy_joint': [],
            'Median_joint': [],
            'Median_Absolute_Deviation_joint': [],
            'Nr_of_Probes': [],
            'Class': []
    }

    # FILL CLASS and NR OF PROBES
    for l in f_clients_only:
        data['Class'].append('Clients')
        data['Nr_of_Probes'].append(0)
    for l in f_sessions:
        data['Class'].append('Probing')
        data['Nr_of_Probes'].append(int(l[2]))

    # MINMAX FETCH
    minmax_clients = []
    minmax_sessions = []
    for l in f_clients_only:
        data['Minimum_fetch'].append(min(l[1]))
        data['Maximum_fetch'].append(max(l[1]))
        minmax_clients.append([min(l[1]),max(l[1])])
    for l in f_sessions:
        data['Minimum_fetch'].append(min(l[1]))
        data['Maximum_fetch'].append(max(l[1]))
        minmax_sessions.append([min(l[1]),max(l[1])])

    fout.write('\n# Minimum and Maximum\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(minmax_clients,minmax_sessions,'Min_Max_Fetch')
    fout.write('|')

    # MINMAX REPLY
    minmax_clients = []
    minmax_sessions = []
    for l in r_clients_only:
        data['Minimum_reply'].append(min(l[1]))
        data['Maximum_reply'].append(max(l[1]))
        minmax_clients.append([min(l[1]),max(l[1])])
    for l in r_sessions:
        data['Minimum_reply'].append(min(l[1]))
        data['Maximum_reply'].append(max(l[1]))
        minmax_sessions.append([min(l[1]),max(l[1])])

    # plotGraph(minmax_clients,minmax_sessions,'Min_Max_Reply')
    fout.write('|')

    # MINMAX JOINT
    minmax_clients = []
    minmax_sessions = []
    for l in j_clients_only:
        data['Minimum_joint'].append(min(l[1]))
        data['Maximum_joint'].append(max(l[1]))
        minmax_clients.append([min(l[1]),max(l[1])])
    for l in j_sessions:
        data['Minimum_joint'].append(min(l[1]))
        data['Maximum_joint'].append(max(l[1]))
        minmax_sessions.append([min(l[1]),max(l[1])])

    # plotGraph(minmax_clients,minmax_sessions,'Min_Max_Joint')
    fout.write('|')

    # MEAN FETCH
    mean_clients = []
    mean_sessions = []
    for l in f_clients_only:
        mean_clients.append(st.tmean(l[1]))
    for l in f_sessions:
        mean_sessions.append(st.tmean(l[1]))
    
    data['Mean_fetch'].extend(mean_clients)
    data['Mean_fetch'].extend(mean_sessions)

    fout.write('\n# Mean\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(mean_clients,mean_sessions,'Mean_Fetch')
    fout.write('|')

    # MEAN REPLY
    mean_clients = []
    mean_sessions = []
    for l in r_clients_only:
        mean_clients.append(st.tmean(l[1]))
    for l in r_sessions:
        mean_sessions.append(st.tmean(l[1]))
    
    data['Mean_reply'].extend(mean_clients)
    data['Mean_reply'].extend(mean_sessions)

    # plotGraph(mean_clients,mean_sessions,'Mean_Reply')
    fout.write('|')

    # MEAN JOINT
    mean_clients = []
    mean_sessions = []
    for l in j_clients_only:
        mean_clients.append(st.tmean(l[1]))
    for l in j_sessions:
        mean_sessions.append(st.tmean(l[1]))

    data['Mean_joint'].extend(mean_clients)
    data['Mean_joint'].extend(mean_sessions)

    # plotGraph(mean_clients,mean_sessions,'Mean_Joint')
    fout.write('|')

    # VARIANCE FETCH
    variance_clients = []
    variance_sessions = []
    for l in f_clients_only:
        variance_clients.append(st.tvar(l[1]))
    for l in f_sessions:
        variance_sessions.append(st.tvar(l[1]))
    
    data['Variance_fetch'].extend(variance_clients)
    data['Variance_fetch'].extend(variance_sessions)

    fout.write('\n# Variance\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(variance_clients,variance_sessions,'Variance_Fetch')
    fout.write('|')

    # VARIANCE REPLY
    variance_clients = []
    variance_sessions = []
    for l in r_clients_only:
        variance_clients.append(st.tvar(l[1]))
    for l in r_sessions:
        variance_sessions.append(st.tvar(l[1]))

    data['Variance_reply'].extend(variance_clients)
    data['Variance_reply'].extend(variance_sessions)

    # plotGraph(variance_clients,variance_sessions,'Variance_Reply')
    fout.write('|')

    # VARIANCE JOINT
    variance_clients = []
    variance_sessions = []
    for l in j_clients_only:
        variance_clients.append(st.tvar(l[1]))
    for l in j_sessions:
        variance_sessions.append(st.tvar(l[1]))

    data['Variance_joint'].extend(variance_clients)
    data['Variance_joint'].extend(variance_sessions)

    # plotGraph(variance_clients,variance_sessions,'Variance_Joint')
    fout.write('|')

    # SKEWNESS FETCH
    skewness_clients = []
    skewness_sessions= []
    for l in f_clients_only:
        skewness_clients.append(st.skew(l[1]))
    for l in f_sessions:
        skewness_sessions.append(st.skew(l[1]))

    data['Skewness_fetch'].extend(skewness_clients)
    data['Skewness_fetch'].extend(skewness_sessions)

    fout.write('\n# Skewness\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(skewness_clients,skewness_sessions,'Skewness_Fetch')
    fout.write('|')

    # SKEWNESS REPLY
    skewness_clients = []
    skewness_sessions= []
    for l in r_clients_only:
        skewness_clients.append(st.skew(l[1]))
    for l in r_sessions:
        skewness_sessions.append(st.skew(l[1]))

    data['Skewness_reply'].extend(skewness_clients)
    data['Skewness_reply'].extend(skewness_sessions)

    # plotGraph(skewness_clients,skewness_sessions,'Skewness_Reply')
    fout.write('|')

    # SKEWNESS JOINT
    skewness_clients = []
    skewness_sessions= []
    for l in j_clients_only:
        skewness_clients.append(st.skew(l[1]))
    for l in j_sessions:
        skewness_sessions.append(st.skew(l[1]))

    data['Skewness_joint'].extend(skewness_clients)
    data['Skewness_joint'].extend(skewness_sessions)

    # plotGraph(skewness_clients,skewness_sessions,'Skewness_Joint')
    fout.write('|')

    # KURTOSIS FECTH
    kurtosis_clients = []
    kurtosis_sessions = []
    for l in f_clients_only:
        kurtosis_clients.append(st.kurtosis(l[1]))
    for l in f_sessions:
        kurtosis_sessions.append(st.kurtosis(l[1]))

    data['Kurtosis_fetch'].extend(kurtosis_clients)
    data['Kurtosis_fetch'].extend(kurtosis_sessions)

    fout.write('\n# Kurtosis\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(kurtosis_clients,kurtosis_sessions,'Kurtosis_Fetch')
    fout.write('|')

    # KURTOSIS REPLY
    kurtosis_clients = []
    kurtosis_sessions = []
    for l in r_clients_only:
        kurtosis_clients.append(st.kurtosis(l[1]))
    for l in r_sessions:
        kurtosis_sessions.append(st.kurtosis(l[1]))

    data['Kurtosis_reply'].extend(kurtosis_clients)
    data['Kurtosis_reply'].extend(kurtosis_sessions)

    # plotGraph(kurtosis_clients,kurtosis_sessions,'Kurtosis_Reply')
    fout.write('|')

    # KURTOSIS JOINT
    kurtosis_clients = []
    kurtosis_sessions = []
    for l in j_clients_only:
        kurtosis_clients.append(st.kurtosis(l[1]))
    for l in j_sessions:
        kurtosis_sessions.append(st.kurtosis(l[1]))

    data['Kurtosis_joint'].extend(kurtosis_clients)
    data['Kurtosis_joint'].extend(kurtosis_sessions)

    # plotGraph(kurtosis_clients,kurtosis_sessions,'Kurtosis_Joint')
    fout.write('|')

    # GMEAN() FETCH
    gmean_clients = []
    gmean_sessions = []
    for l in f_clients_only:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        gmean_clients.append(st.gmean(lst))
    for l in f_sessions:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        gmean_sessions.append(st.gmean(lst))

    data['Geometric_Mean_fetch'].extend(gmean_clients)
    data['Geometric_Mean_fetch'].extend(gmean_sessions)

    fout.write('\n# Geometric Mean\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(gmean_clients,gmean_sessions,'Geometric_Mean_Fetch')
    fout.write('|')

    # GMEAN() REPLY
    gmean_clients = []
    gmean_sessions = []

    for l in r_clients_only:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        gmean_clients.append(st.gmean(lst))
    for l in r_sessions:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        gmean_sessions.append(st.gmean(lst))

    data['Geometric_Mean_reply'].extend(gmean_clients)
    data['Geometric_Mean_reply'].extend(gmean_sessions)

    # plotGraph(gmean_clients,gmean_sessions,'Geometric_Mean_Reply')
    fout.write('|')

    # GMEAN() JOINT
    gmean_clients = []
    gmean_sessions = []

    for l in j_clients_only:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        gmean_clients.append(st.gmean(lst))
    for l in j_sessions:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        gmean_sessions.append(st.gmean(lst))

    data['Geometric_Mean_joint'].extend(gmean_clients)
    data['Geometric_Mean_joint'].extend(gmean_sessions)

    # plotGraph(gmean_clients,gmean_sessions,'Geometric_Mean_Joint')
    fout.write('|')

    # HMEAN() FETCH
    hmean_clients = []
    hmean_sessions = []

    for l in f_clients_only:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        hmean = st.hmean(lst)
        hmean_clients.append(hmean)
    for l in f_sessions:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        hmean = st.hmean(lst)
        hmean_sessions.append(hmean)

    data['Harmonic_Mean_fetch'].extend(hmean_clients)
    data['Harmonic_Mean_fetch'].extend(hmean_sessions)

    fout.write('\n# Harmonic Mean\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(hmean_clients,hmean_sessions,'Harmonic_Mean_Fetch')
    fout.write('|')

    # HMEAN() REPLY
    hmean_clients = []
    hmean_sessions = []

    for l in r_clients_only:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        hmean = st.hmean(lst)
        hmean_clients.append(hmean)
    for l in r_sessions:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        hmean = st.hmean(lst)
        hmean_sessions.append(hmean)

    data['Harmonic_Mean_reply'].extend(hmean_clients)
    data['Harmonic_Mean_reply'].extend(hmean_sessions)

    # plotGraph(hmean_clients,hmean_sessions,'Harmonic_Mean_Reply')
    fout.write('|')

    # HMEAN() JOINT
    hmean_clients = []
    hmean_sessions = []

    for l in j_clients_only:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        hmean = st.hmean(lst)
        hmean_clients.append(hmean)
    for l in j_sessions:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        hmean = st.hmean(lst)
        hmean_sessions.append(hmean)

    data['Harmonic_Mean_joint'].extend(hmean_clients)
    data['Harmonic_Mean_joint'].extend(hmean_sessions)

    # plotGraph(hmean_clients,hmean_sessions,'Harmonic_Mean_Joint')
    fout.write('|')

    # MODE() FETCH
    f_mode_clients = []
    f_mode_sessions = []
    f_mode_count_clients = []
    f_mode_count_sessions = []

    for l in f_clients_only:
        mode, count = st.mode(l[1],axis=None)
        f_mode_clients.extend(mode)
        f_mode_count_clients.extend(count)
    for l in f_sessions:
        mode, count = st.mode(l[1],axis=None)
        f_mode_sessions.extend(mode)
        f_mode_count_sessions.extend(count)

    # MODE() REPLY
    r_mode_clients = []
    r_mode_sessions = []
    r_mode_count_clients = []
    r_mode_count_sessions = []

    for l in r_clients_only:
        mode, count = st.mode(l[1],axis=None)
        r_mode_clients.extend(mode)
        r_mode_count_clients.extend(count)
    for l in r_sessions:
        mode, count = st.mode(l[1],axis=None)
        r_mode_sessions.extend(mode)
        r_mode_count_sessions.extend(count)

    # MODE() JOINT
    j_mode_clients = []
    j_mode_sessions = []
    j_mode_count_clients = []
    j_mode_count_sessions = []

    for l in j_clients_only:
        mode, count = st.mode(l[1],axis=None)
        j_mode_clients.extend(mode)
        j_mode_count_clients.extend(count)
    for l in j_sessions:
        mode, count = st.mode(l[1],axis=None)
        j_mode_sessions.extend(mode)
        j_mode_count_sessions.extend(count)

    fout.write('\n# Mode\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_mode_clients,f_mode_sessions,'Mode_Fetch')
    fout.write('|')
    # plotGraph(r_mode_clients,r_mode_sessions,'Mode_Reply')
    fout.write('|')
    # plotGraph(j_mode_clients,j_mode_sessions,'Mode_Joint')
    fout.write('|')

    data['Mode_fetch'].extend(f_mode_clients)
    data['Mode_fetch'].extend(f_mode_sessions)
    data['Mode_reply'].extend(r_mode_clients)
    data['Mode_reply'].extend(r_mode_sessions)
    data['Mode_joint'].extend(j_mode_clients)
    data['Mode_joint'].extend(j_mode_sessions)

    fout.write('\n# Mode Count\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_mode_count_clients,f_mode_count_sessions,'Mode_Count_Fetch')
    fout.write('|')
    # plotGraph(r_mode_count_clients,r_mode_count_sessions,'Mode_Count_Reply')
    fout.write('|')
    # plotGraph(j_mode_count_clients,j_mode_count_sessions,'Mode_Count_Joint')
    fout.write('|')

    data['Mode_Count_fetch'].extend(f_mode_count_clients)
    data['Mode_Count_fetch'].extend(f_mode_count_sessions)
    data['Mode_Count_reply'].extend(r_mode_count_clients)
    data['Mode_Count_reply'].extend(r_mode_count_sessions)
    data['Mode_Count_joint'].extend(j_mode_count_clients)
    data['Mode_Count_joint'].extend(j_mode_count_sessions)

    # MOMENT() FETCH
    moment_clients = []
    moment_sessions = []

    for l in f_clients_only:
        moment = st.moment(l[1])
        moment_clients.append(moment)
    for l in f_sessions:
        moment = st.moment(l[1])
        moment_sessions.append(moment)

    data['Moment_fetch'].extend(moment_clients)
    data['Moment_fetch'].extend(moment_sessions)

    fout.write('\n# Moment\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(moment_clients,moment_sessions,'Moment_Fetch')
    fout.write('|')

    # MOMENT() REPLY
    moment_clients = []
    moment_sessions = []

    for l in r_clients_only:
        moment = st.moment(l[1])
        moment_clients.append(moment)
    for l in r_sessions:
        moment = st.moment(l[1])
        moment_sessions.append(moment)    

    data['Moment_reply'].extend(moment_clients)
    data['Moment_reply'].extend(moment_sessions)

    # plotGraph(moment_clients,moment_sessions,'Moment_Reply')
    fout.write('|')

    # MOMENT() JOINT
    moment_clients = []
    moment_sessions = []

    for l in j_clients_only:
        moment = st.moment(l[1])
        moment_clients.append(moment)
    for l in j_sessions:
        moment = st.moment(l[1])
        moment_sessions.append(moment)    

    data['Moment_joint'].extend(moment_clients)
    data['Moment_joint'].extend(moment_sessions)

    # plotGraph(moment_clients,moment_sessions,'Moment_Joint')
    fout.write('|')

    # KSTAT() FETCH
    f_kstat1_clients = []
    f_kstat1_sessions = []
    f_kstat2_clients = []
    f_kstat2_sessions = []
    f_kstat3_clients = []
    f_kstat3_sessions = []
    f_kstat4_clients = []
    f_kstat4_sessions = []

    for l in f_clients_only:
        f_kstat1_clients.append(st.kstat(l[1],1))
        f_kstat2_clients.append(st.kstat(l[1],2))
        f_kstat3_clients.append(st.kstat(l[1],3))
        f_kstat4_clients.append(st.kstat(l[1],4))
    for l in f_sessions:
        f_kstat1_sessions.append(st.kstat(l[1],1))
        f_kstat2_sessions.append(st.kstat(l[1],2))
        f_kstat3_sessions.append(st.kstat(l[1],3))
        f_kstat4_sessions.append(st.kstat(l[1],4))

    # KSTAT() REPLY
    r_kstat1_clients = []
    r_kstat1_sessions = []
    r_kstat2_clients = []
    r_kstat2_sessions = []
    r_kstat3_clients = []
    r_kstat3_sessions = []
    r_kstat4_clients = []
    r_kstat4_sessions = []

    for l in r_clients_only:
        r_kstat1_clients.append(st.kstat(l[1],1))
        r_kstat2_clients.append(st.kstat(l[1],2))
        r_kstat3_clients.append(st.kstat(l[1],3))
        r_kstat4_clients.append(st.kstat(l[1],4))
    for l in r_sessions:
        r_kstat1_sessions.append(st.kstat(l[1],1))
        r_kstat2_sessions.append(st.kstat(l[1],2))
        r_kstat3_sessions.append(st.kstat(l[1],3))
        r_kstat4_sessions.append(st.kstat(l[1],4))
    
    # KSTAT() JOINT
    j_kstat1_clients = []
    j_kstat1_sessions = []
    j_kstat2_clients = []
    j_kstat2_sessions = []
    j_kstat3_clients = []
    j_kstat3_sessions = []
    j_kstat4_clients = []
    j_kstat4_sessions = []

    for l in j_clients_only:
        j_kstat1_clients.append(st.kstat(l[1],1))
        j_kstat2_clients.append(st.kstat(l[1],2))
        j_kstat3_clients.append(st.kstat(l[1],3))
        j_kstat4_clients.append(st.kstat(l[1],4))
    for l in j_sessions:
        j_kstat1_sessions.append(st.kstat(l[1],1))
        j_kstat2_sessions.append(st.kstat(l[1],2))
        j_kstat3_sessions.append(st.kstat(l[1],3))
        j_kstat4_sessions.append(st.kstat(l[1],4))

    fout.write('\n# Kth-Statistic, n=1\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_kstat1_clients,f_kstat1_sessions,'kstat_n1_Fetch')
    fout.write('|')
    # plotGraph(r_kstat1_clients,r_kstat1_sessions,'kstat_n1_Reply')
    fout.write('|')
    # plotGraph(j_kstat1_clients,j_kstat1_sessions,'kstat_n1_Joint')
    fout.write('|')

    data['Kth-Stat_n1_fetch'].extend(f_kstat1_clients)
    data['Kth-Stat_n1_fetch'].extend(f_kstat1_sessions)
    data['Kth-Stat_n1_reply'].extend(r_kstat1_clients)
    data['Kth-Stat_n1_reply'].extend(r_kstat1_sessions)
    data['Kth-Stat_n1_joint'].extend(j_kstat1_clients)
    data['Kth-Stat_n1_joint'].extend(j_kstat1_sessions)

    fout.write('\n# Kth-Statistic, n=2\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_kstat2_clients,f_kstat2_sessions,'kstat_n2_Fetch')
    fout.write('|')
    # plotGraph(r_kstat2_clients,r_kstat2_sessions,'kstat_n2_Reply')
    fout.write('|')
    # plotGraph(j_kstat2_clients,j_kstat2_sessions,'kstat_n2_Joint')
    fout.write('|')

    data['Kth-Stat_n2_fetch'].extend(f_kstat2_clients)
    data['Kth-Stat_n2_fetch'].extend(f_kstat2_sessions)
    data['Kth-Stat_n2_reply'].extend(r_kstat2_clients)
    data['Kth-Stat_n2_reply'].extend(r_kstat2_sessions)
    data['Kth-Stat_n2_joint'].extend(j_kstat2_clients)
    data['Kth-Stat_n2_joint'].extend(j_kstat2_sessions)

    fout.write('\n# Kth-Statistic, n=3\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_kstat3_clients,f_kstat3_sessions,'kstat_n3_Fetch')
    fout.write('|')
    # plotGraph(r_kstat3_clients,r_kstat3_sessions,'kstat_n3_Reply')
    fout.write('|')
    # plotGraph(j_kstat3_clients,j_kstat3_sessions,'kstat_n3_Joint')
    fout.write('|')

    data['Kth-Stat_n3_fetch'].extend(f_kstat3_clients)
    data['Kth-Stat_n3_fetch'].extend(f_kstat3_sessions)
    data['Kth-Stat_n3_reply'].extend(r_kstat3_clients)
    data['Kth-Stat_n3_reply'].extend(r_kstat3_sessions)
    data['Kth-Stat_n3_joint'].extend(j_kstat3_clients)
    data['Kth-Stat_n3_joint'].extend(j_kstat3_sessions)

    fout.write('\n# Kth-Statistic, n=4\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_kstat4_clients,f_kstat4_sessions,'kstat_n4_Fetch')
    fout.write('|')
    # plotGraph(r_kstat4_clients,r_kstat4_sessions,'kstat_n4_Reply')
    fout.write('|')
    # plotGraph(j_kstat4_clients,j_kstat4_sessions,'kstat_n4_Joint')
    fout.write('|')

    data['Kth-Stat_n4_fetch'].extend(f_kstat4_clients)
    data['Kth-Stat_n4_fetch'].extend(f_kstat4_sessions)
    data['Kth-Stat_n4_reply'].extend(r_kstat4_clients)
    data['Kth-Stat_n4_reply'].extend(r_kstat4_sessions)
    data['Kth-Stat_n4_joint'].extend(j_kstat4_clients)
    data['Kth-Stat_n4_joint'].extend(j_kstat4_sessions)

    # KSTATVAR() FETCH
    f_kstatvar1_clients = []
    f_kstatvar1_sessions = []
    f_kstatvar2_clients = []
    f_kstatvar2_sessions = []

    for l in f_clients_only:
        f_kstatvar1_clients.append(st.kstatvar(l[1],1))
        f_kstatvar2_clients.append(st.kstatvar(l[1],2))
    for l in f_sessions:
        f_kstatvar1_sessions.append(st.kstatvar(l[1],1))
        f_kstatvar2_sessions.append(st.kstatvar(l[1],2))

    # KSTATVAR() REPLY
    r_kstatvar1_clients = []
    r_kstatvar1_sessions = []
    r_kstatvar2_clients = []
    r_kstatvar2_sessions = []

    for l in r_clients_only:
        r_kstatvar1_clients.append(st.kstatvar(l[1],1))
        r_kstatvar2_clients.append(st.kstatvar(l[1],2))
    for l in r_sessions:
        r_kstatvar1_sessions.append(st.kstatvar(l[1],1))
        r_kstatvar2_sessions.append(st.kstatvar(l[1],2))

    # KSTATVAR() JOINT
    j_kstatvar1_clients = []
    j_kstatvar1_sessions = []
    j_kstatvar2_clients = []
    j_kstatvar2_sessions = []

    for l in j_clients_only:
        j_kstatvar1_clients.append(st.kstatvar(l[1],1))
        j_kstatvar2_clients.append(st.kstatvar(l[1],2))
    for l in j_sessions:
        j_kstatvar1_sessions.append(st.kstatvar(l[1],1))
        j_kstatvar2_sessions.append(st.kstatvar(l[1],2))

    fout.write('\n# Kth-Statistic variance, n=1\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_kstatvar1_clients,f_kstatvar1_sessions,'kstat_variance_n1_Fetch')
    fout.write('|')
    # plotGraph(r_kstatvar1_clients,r_kstatvar1_sessions,'kstat_variance_n1_Reply')
    fout.write('|')
    # plotGraph(j_kstatvar1_clients,j_kstatvar1_sessions,'kstat_variance_n1_Joint')
    fout.write('|')

    data['Kth-Stat_Variance_n1_fetch'].extend(f_kstatvar1_clients)
    data['Kth-Stat_Variance_n1_fetch'].extend(f_kstatvar1_sessions)
    data['Kth-Stat_Variance_n1_reply'].extend(r_kstatvar1_clients)
    data['Kth-Stat_Variance_n1_reply'].extend(r_kstatvar1_sessions)
    data['Kth-Stat_Variance_n1_joint'].extend(j_kstatvar1_clients)
    data['Kth-Stat_Variance_n1_joint'].extend(j_kstatvar1_sessions)

    fout.write('\n# Kth-Statistic variance, n=2\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_kstatvar2_clients,f_kstatvar2_sessions,'kstat_variance_n2_Fetch')
    fout.write('|')
    # plotGraph(r_kstatvar2_clients,r_kstatvar2_sessions,'kstat_variance_n2_Reply')
    fout.write('|')
    # plotGraph(j_kstatvar2_clients,j_kstatvar2_sessions,'kstat_variance_n2_Joint')
    fout.write('|')

    data['Kth-Stat_Variance_n2_fetch'].extend(f_kstatvar2_clients)
    data['Kth-Stat_Variance_n2_fetch'].extend(f_kstatvar2_sessions)
    data['Kth-Stat_Variance_n2_reply'].extend(r_kstatvar2_clients)
    data['Kth-Stat_Variance_n2_reply'].extend(r_kstatvar2_sessions)
    data['Kth-Stat_Variance_n2_joint'].extend(j_kstatvar2_clients)
    data['Kth-Stat_Variance_n2_joint'].extend(j_kstatvar2_sessions)

    # GSTD() FETCH
    gstd_clients = []
    gstd_sessions = []

    for l in f_clients_only:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        if lst == []: continue
        gstd = st.gstd(lst)
        gstd_clients.append(gstd)
    for l in f_sessions:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        if lst == []: continue
        gstd = st.gstd(lst)
        gstd_sessions.append(gstd)
    
    data['Geometric_Standard_Deviation_fetch'].extend(gstd_clients)
    data['Geometric_Standard_Deviation_fetch'].extend(gstd_sessions)

    fout.write('\n# Geometric Standard Deviation\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(gstd_clients,gstd_sessions,'Geometric_Standard_Deviation_Fetch')
    fout.write('|')

    # GSTD() REPLY
    gstd_clients = []
    gstd_sessions = []

    for l in r_clients_only:
        if lst == []: continue
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        if lst == []: continue
        gstd = st.gstd(lst)
        gstd_clients.append(gstd)
    for l in r_sessions:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        if lst == []: continue
        gstd = st.gstd(lst)
        gstd_sessions.append(gstd)

    data['Geometric_Standard_Deviation_reply'].extend(gstd_clients)
    data['Geometric_Standard_Deviation_reply'].extend(gstd_sessions)

    # plotGraph(gstd_clients,gstd_sessions,'Geometric_Standard_Deviation_Reply')
    fout.write('|')

    # GSTD() JOINT
    gstd_clients = []
    gstd_sessions = []

    for l in j_clients_only:
        if lst == []: continue
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        if lst == []: continue
        gstd = st.gstd(lst)
        gstd_clients.append(gstd)
    for l in j_sessions:
        lst = []
        for e in l[1]:
            if e == 0: continue
            elif e < 0: val = e * -1
            else: val = e
            lst.append(val)
        if lst == []: continue
        gstd = st.gstd(lst)
        gstd_sessions.append(gstd)

    data['Geometric_Standard_Deviation_joint'].extend(gstd_clients)
    data['Geometric_Standard_Deviation_joint'].extend(gstd_sessions)

    # plotGraph(gstd_clients,gstd_sessions,'Geometric_Standard_Deviation_Joint')
    fout.write('|')

    # IQR() FETCH
    f_iqr25_75_clients = []
    f_iqr25_75_sessions = []
    f_iqr5_95_clients = []
    f_iqr5_95_sessions = []

    for l in f_clients_only:
        iqr = st.iqr(l[1],rng=(25,75))
        f_iqr25_75_clients.append(iqr)
        iqr = st.iqr(l[1],rng=(5,95))
        f_iqr5_95_clients.append(iqr)
    for l in f_sessions:
        iqr = st.iqr(l[1],rng=(25,75))
        f_iqr25_75_sessions.append(iqr)
        iqr = st.iqr(l[1],rng=(5,95))
        f_iqr5_95_sessions.append(iqr)
    
    # IQR() REPLY
    r_iqr25_75_clients = []
    r_iqr25_75_sessions = []
    r_iqr5_95_clients = []
    r_iqr5_95_sessions = []

    for l in r_clients_only:
        iqr = st.iqr(l[1],rng=(25,75))
        r_iqr25_75_clients.append(iqr)
        iqr = st.iqr(l[1],rng=(5,95))
        r_iqr5_95_clients.append(iqr)
    for l in r_sessions:
        iqr = st.iqr(l[1],rng=(25,75))
        r_iqr25_75_sessions.append(iqr)
        iqr = st.iqr(l[1],rng=(5,95))
        r_iqr5_95_sessions.append(iqr)
    
    # IQR() JOINT
    j_iqr25_75_clients = []
    j_iqr25_75_sessions = []
    j_iqr5_95_clients = []
    j_iqr5_95_sessions = []

    for l in j_clients_only:
        iqr = st.iqr(l[1],rng=(25,75))
        j_iqr25_75_clients.append(iqr)
        iqr = st.iqr(l[1],rng=(5,95))
        j_iqr5_95_clients.append(iqr)
    for l in j_sessions:
        iqr = st.iqr(l[1],rng=(25,75))
        j_iqr25_75_sessions.append(iqr)
        iqr = st.iqr(l[1],rng=(5,95))
        j_iqr5_95_sessions.append(iqr)

    fout.write('\n# Inter-Quartile Range (25%\-75%)\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_iqr25_75_clients,f_iqr25_75_sessions,'Percentile_25_75_Fetch')
    fout.write('|')
    # plotGraph(r_iqr25_75_clients,r_iqr25_75_sessions,'Percentile_25_75_Reply')
    fout.write('|')
    # plotGraph(j_iqr25_75_clients,j_iqr25_75_sessions,'Percentile_25_75_Joint')
    fout.write('|')

    data['IQR_25_75_fetch'].extend(f_iqr25_75_clients)
    data['IQR_25_75_fetch'].extend(f_iqr25_75_sessions)
    data['IQR_25_75_reply'].extend(r_iqr25_75_clients)
    data['IQR_25_75_reply'].extend(r_iqr25_75_sessions)
    data['IQR_25_75_joint'].extend(j_iqr25_75_clients)
    data['IQR_25_75_joint'].extend(j_iqr25_75_sessions)

    fout.write('\n# Inter-Quartile Range (5%\-95%)\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_iqr5_95_clients,f_iqr5_95_sessions,'Percentile_5_95_Fetch')
    fout.write('|')
    # plotGraph(r_iqr5_95_clients,r_iqr5_95_sessions,'Percentile_5_95_Reply')
    fout.write('|')
    # plotGraph(j_iqr5_95_clients,j_iqr5_95_sessions,'Percentile_5_95_Joint')
    fout.write('|')

    data['IQR_5_95_fetch'].extend(f_iqr5_95_clients)
    data['IQR_5_95_fetch'].extend(f_iqr5_95_sessions)
    data['IQR_5_95_reply'].extend(r_iqr5_95_clients)
    data['IQR_5_95_reply'].extend(r_iqr5_95_sessions)
    data['IQR_5_95_joint'].extend(j_iqr5_95_clients)
    data['IQR_5_95_joint'].extend(j_iqr5_95_sessions)

    # SEM() FETCH
    sem_clients = []
    sem_sessions = []

    for l in f_clients_only:
        sem = st.sem(l[1])
        sem_clients.append(sem)
    for l in f_sessions:
        sem = st.sem(l[1])
        sem_sessions.append(sem)
    
    data['Standard_Error_Mean_fetch'].extend(sem_clients)
    data['Standard_Error_Mean_fetch'].extend(sem_sessions)

    fout.write('\n# Standard Error of the Mean\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(sem_clients,sem_sessions,'Standard_Error_Mean_Fetch')
    fout.write('|')

    # SEM() REPLY
    sem_clients = []
    sem_sessions = []

    for l in r_clients_only:
        sem = st.sem(l[1])
        sem_clients.append(sem)
    for l in r_sessions:
        sem = st.sem(l[1])
        sem_sessions.append(sem)

    data['Standard_Error_Mean_reply'].extend(sem_clients)
    data['Standard_Error_Mean_reply'].extend(sem_sessions)

    # plotGraph(sem_clients,sem_sessions,'Standard_Error_Mean_Reply')
    fout.write('|')

    # SEM() JOINT
    sem_clients = []
    sem_sessions = []

    for l in j_clients_only:
        sem = st.sem(l[1])
        sem_clients.append(sem)
    for l in j_sessions:
        sem = st.sem(l[1])
        sem_sessions.append(sem)

    data['Standard_Error_Mean_joint'].extend(sem_clients)
    data['Standard_Error_Mean_joint'].extend(sem_sessions)

    # plotGraph(sem_clients,sem_sessions,'Standard_Error_Mean_Joint')
    fout.write('|')

    # BAYES_MVS() FETCH
    f_mean_cntr_clients = []
    f_mean_cntr_sessions = []
    f_var_cntr_clients = []
    f_var_cntr_sessions = []
    f_std_cntr_clients = []
    f_std_cntr_sessions = []

    for l in f_clients_only:
        if len(l[1]) < 2:
            data['BCI_Mean_center_fetch'].append(None)
            data['BCI_Mean_upper_bound_fetch'].append(None)
            data['BCI_Mean_lower_bound_fetch'].append(None)
            data['BCI_Variance_center_fetch'].append(None)
            data['BCI_Variance_upper_bound_fetch'].append(None)
            data['BCI_Variance_lower_bound_fetch'].append(None)
            data['BCI_Standard_Deviation_center_fetch'].append(None)
            data['BCI_Standard_Deviation_upper_bound_fetch'].append(None)
            data['BCI_Standard_Deviation_lower_bound_fetch'].append(None)
            continue
        mean_cntr, var_cntr, std_cntr = st.bayes_mvs(l[1])
        data['BCI_Mean_center_fetch'].append(mean_cntr[0])
        data['BCI_Mean_upper_bound_fetch'].append(mean_cntr[1][1])
        data['BCI_Mean_lower_bound_fetch'].append(mean_cntr[1][0])
        data['BCI_Variance_center_fetch'].append(var_cntr[0])
        data['BCI_Variance_upper_bound_fetch'].append(var_cntr[1][1])
        data['BCI_Variance_lower_bound_fetch'].append(var_cntr[1][0])
        data['BCI_Standard_Deviation_center_fetch'].append(std_cntr[0])
        data['BCI_Standard_Deviation_upper_bound_fetch'].append(std_cntr[1][1])
        data['BCI_Standard_Deviation_lower_bound_fetch'].append(std_cntr[1][0])
        f_mean_cntr_clients.append(mean_cntr)
        f_var_cntr_clients.append(var_cntr)
        f_std_cntr_clients.append(std_cntr)
    for l in f_sessions:
        if len(l[1]) < 2: 
            data['BCI_Mean_center_fetch'].append(None)
            data['BCI_Mean_upper_bound_fetch'].append(None)
            data['BCI_Mean_lower_bound_fetch'].append(None)
            data['BCI_Variance_center_fetch'].append(None)
            data['BCI_Variance_upper_bound_fetch'].append(None)
            data['BCI_Variance_lower_bound_fetch'].append(None)
            data['BCI_Standard_Deviation_center_fetch'].append(None)
            data['BCI_Standard_Deviation_upper_bound_fetch'].append(None)
            data['BCI_Standard_Deviation_lower_bound_fetch'].append(None)
            continue
        mean_cntr, var_cntr, std_cntr = st.bayes_mvs(l[1])
        data['BCI_Mean_center_fetch'].append(mean_cntr[0])
        data['BCI_Mean_upper_bound_fetch'].append(mean_cntr[1][1])
        data['BCI_Mean_lower_bound_fetch'].append(mean_cntr[1][0])
        data['BCI_Variance_center_fetch'].append(var_cntr[0])
        data['BCI_Variance_upper_bound_fetch'].append(var_cntr[1][1])
        data['BCI_Variance_lower_bound_fetch'].append(var_cntr[1][0])
        data['BCI_Standard_Deviation_center_fetch'].append(std_cntr[0])
        data['BCI_Standard_Deviation_upper_bound_fetch'].append(std_cntr[1][1])
        data['BCI_Standard_Deviation_lower_bound_fetch'].append(std_cntr[1][0])
        f_mean_cntr_sessions.append(mean_cntr)
        f_var_cntr_sessions.append(var_cntr)
        f_std_cntr_sessions.append(std_cntr)

    # BAYES_MVS() REPLY
    r_mean_cntr_clients = []
    r_mean_cntr_sessions = []
    r_var_cntr_clients = []
    r_var_cntr_sessions = []
    r_std_cntr_clients = []
    r_std_cntr_sessions = []

    for l in r_clients_only:
        if len(l[1]) < 2: 
            data['BCI_Mean_center_reply'].append(None)
            data['BCI_Mean_upper_bound_reply'].append(None)
            data['BCI_Mean_lower_bound_reply'].append(None)
            data['BCI_Variance_center_reply'].append(None)
            data['BCI_Variance_upper_bound_reply'].append(None)
            data['BCI_Variance_lower_bound_reply'].append(None)
            data['BCI_Standard_Deviation_center_reply'].append(None)
            data['BCI_Standard_Deviation_upper_bound_reply'].append(None)
            data['BCI_Standard_Deviation_lower_bound_reply'].append(None)
            continue
        mean_cntr, var_cntr, std_cntr = st.bayes_mvs(l[1])
        data['BCI_Mean_center_reply'].append(mean_cntr[0])
        data['BCI_Mean_upper_bound_reply'].append(mean_cntr[1][1])
        data['BCI_Mean_lower_bound_reply'].append(mean_cntr[1][0])
        data['BCI_Variance_center_reply'].append(var_cntr[0])
        data['BCI_Variance_upper_bound_reply'].append(var_cntr[1][1])
        data['BCI_Variance_lower_bound_reply'].append(var_cntr[1][0])
        data['BCI_Standard_Deviation_center_reply'].append(std_cntr[0])
        data['BCI_Standard_Deviation_upper_bound_reply'].append(std_cntr[1][1])
        data['BCI_Standard_Deviation_lower_bound_reply'].append(std_cntr[1][0])
        r_mean_cntr_clients.append(mean_cntr)
        r_var_cntr_clients.append(var_cntr)
        r_std_cntr_clients.append(std_cntr)
    for l in r_sessions:
        if len(l[1]) < 2: 
            data['BCI_Mean_center_reply'].append(None)
            data['BCI_Mean_upper_bound_reply'].append(None)
            data['BCI_Mean_lower_bound_reply'].append(None)
            data['BCI_Variance_center_reply'].append(None)
            data['BCI_Variance_upper_bound_reply'].append(None)
            data['BCI_Variance_lower_bound_reply'].append(None)
            data['BCI_Standard_Deviation_center_reply'].append(None)
            data['BCI_Standard_Deviation_upper_bound_reply'].append(None)
            data['BCI_Standard_Deviation_lower_bound_reply'].append(None)
            continue
        mean_cntr, var_cntr, std_cntr = st.bayes_mvs(l[1])
        data['BCI_Mean_center_reply'].append(mean_cntr[0])
        data['BCI_Mean_upper_bound_reply'].append(mean_cntr[1][1])
        data['BCI_Mean_lower_bound_reply'].append(mean_cntr[1][0])
        data['BCI_Variance_center_reply'].append(var_cntr[0])
        data['BCI_Variance_upper_bound_reply'].append(var_cntr[1][1])
        data['BCI_Variance_lower_bound_reply'].append(var_cntr[1][0])
        data['BCI_Standard_Deviation_center_reply'].append(std_cntr[0])
        data['BCI_Standard_Deviation_upper_bound_reply'].append(std_cntr[1][1])
        data['BCI_Standard_Deviation_lower_bound_reply'].append(std_cntr[1][0])
        r_mean_cntr_sessions.append(mean_cntr)
        r_var_cntr_sessions.append(var_cntr)
        r_std_cntr_sessions.append(std_cntr)

    # BAYES_MVS() JOINT
    j_mean_cntr_clients = []
    j_mean_cntr_sessions = []
    j_var_cntr_clients = []
    j_var_cntr_sessions = []
    j_std_cntr_clients = []
    j_std_cntr_sessions = []

    for l in j_clients_only:
        if len(l[1]) < 2: 
            data['BCI_Mean_center_joint'].append(None)
            data['BCI_Mean_upper_bound_joint'].append(None)
            data['BCI_Mean_lower_bound_joint'].append(None)
            data['BCI_Variance_center_joint'].append(None)
            data['BCI_Variance_upper_bound_joint'].append(None)
            data['BCI_Variance_lower_bound_joint'].append(None)
            data['BCI_Standard_Deviation_center_joint'].append(None)
            data['BCI_Standard_Deviation_upper_bound_joint'].append(None)
            data['BCI_Standard_Deviation_lower_bound_joint'].append(None)
            continue
        mean_cntr, var_cntr, std_cntr = st.bayes_mvs(l[1])
        data['BCI_Mean_center_joint'].append(mean_cntr[0])
        data['BCI_Mean_upper_bound_joint'].append(mean_cntr[1][1])
        data['BCI_Mean_lower_bound_joint'].append(mean_cntr[1][0])
        data['BCI_Variance_center_joint'].append(var_cntr[0])
        data['BCI_Variance_upper_bound_joint'].append(var_cntr[1][1])
        data['BCI_Variance_lower_bound_joint'].append(var_cntr[1][0])
        data['BCI_Standard_Deviation_center_joint'].append(std_cntr[0])
        data['BCI_Standard_Deviation_upper_bound_joint'].append(std_cntr[1][1])
        data['BCI_Standard_Deviation_lower_bound_joint'].append(std_cntr[1][0])
        j_mean_cntr_clients.append(mean_cntr)
        j_var_cntr_clients.append(var_cntr)
        j_std_cntr_clients.append(std_cntr)
    for l in j_sessions:
        if len(l[1]) < 2: 
            data['BCI_Mean_center_joint'].append(None)
            data['BCI_Mean_upper_bound_joint'].append(None)
            data['BCI_Mean_lower_bound_joint'].append(None)
            data['BCI_Variance_center_joint'].append(None)
            data['BCI_Variance_upper_bound_joint'].append(None)
            data['BCI_Variance_lower_bound_joint'].append(None)
            data['BCI_Standard_Deviation_center_joint'].append(None)
            data['BCI_Standard_Deviation_upper_bound_joint'].append(None)
            data['BCI_Standard_Deviation_lower_bound_joint'].append(None)
            continue
        mean_cntr, var_cntr, std_cntr = st.bayes_mvs(l[1])
        data['BCI_Mean_center_joint'].append(mean_cntr[0])
        data['BCI_Mean_upper_bound_joint'].append(mean_cntr[1][1])
        data['BCI_Mean_lower_bound_joint'].append(mean_cntr[1][0])
        data['BCI_Variance_center_joint'].append(var_cntr[0])
        data['BCI_Variance_upper_bound_joint'].append(var_cntr[1][1])
        data['BCI_Variance_lower_bound_joint'].append(var_cntr[1][0])
        data['BCI_Standard_Deviation_center_joint'].append(std_cntr[0])
        data['BCI_Standard_Deviation_upper_bound_joint'].append(std_cntr[1][1])
        data['BCI_Standard_Deviation_lower_bound_joint'].append(std_cntr[1][0])
        j_mean_cntr_sessions.append(mean_cntr)
        j_var_cntr_sessions.append(var_cntr)
        j_std_cntr_sessions.append(std_cntr)

    fout.write('\n# Bayesian Confidence Interval - Mean\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_mean_cntr_clients,f_mean_cntr_sessions,'Bayesian_Confidence_Interval_Mean_Fetch')
    fout.write('|')
    # plotGraph(r_mean_cntr_clients,r_mean_cntr_sessions,'Bayesian_Confidence_Interval_Mean_Reply')
    fout.write('|')
    # plotGraph(j_mean_cntr_clients,j_mean_cntr_sessions,'Bayesian_Confidence_Interval_Mean_Joint')
    fout.write('|')

    fout.write('\n# Bayesian Confidence Interval - Variance\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_var_cntr_clients,f_var_cntr_sessions,'Bayesian_Confidence_Interval_Variance_Fetch')
    fout.write('|')
    # plotGraph(r_var_cntr_clients,r_var_cntr_sessions,'Bayesian_Confidence_Interval_Variance_Reply')
    fout.write('|')
    # plotGraph(j_var_cntr_clients,j_var_cntr_sessions,'Bayesian_Confidence_Interval_Variance_Joint')
    fout.write('|')

    fout.write('\n# Bayesian Confidence Interval - Standard Deviation\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(f_std_cntr_clients,f_std_cntr_sessions,'Bayesian_Confidence_Interval_Standard_Deviation_Fetch')
    fout.write('|')
    # plotGraph(r_std_cntr_clients,r_std_cntr_sessions,'Bayesian_Confidence_Interval_Standard_Deviation_Reply')
    fout.write('|')
    # plotGraph(j_std_cntr_clients,j_std_cntr_sessions,'Bayesian_Confidence_Interval_Standard_Deviation_Joint')
    fout.write('|')

    # DIFFERENTIAL_ENTROPY() FETCH
    diff_ent_clients = []
    diff_ent_sessions = []

    for l in f_clients_only:
        diff_ent = st.differential_entropy(l[1])
        diff_ent_clients.append(diff_ent)
    for l in f_sessions:
        diff_ent = st.differential_entropy(l[1])
        diff_ent_sessions.append(diff_ent)

    data['Differential_Entropy_fetch'].extend(diff_ent_clients)
    data['Differential_Entropy_fetch'].extend(diff_ent_sessions)

    fout.write('\n# Differential Entropy\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(diff_ent_clients,diff_ent_sessions,'Differential_Entropy_Fetch')
    fout.write('|')
    
    # DIFFERENTIAL_ENTROPY() REPLY
    diff_ent_clients = []
    diff_ent_sessions = []

    for l in r_clients_only:
        diff_ent = st.differential_entropy(l[1])
        diff_ent_clients.append(diff_ent)
    for l in r_sessions:
        diff_ent = st.differential_entropy(l[1])
        diff_ent_sessions.append(diff_ent)

    data['Differential_Entropy_reply'].extend(diff_ent_clients)
    data['Differential_Entropy_reply'].extend(diff_ent_sessions)

    # plotGraph(diff_ent_clients,diff_ent_sessions,'Differential_Entropy_Reply')
    fout.write('|')

    # DIFFERENTIAL_ENTROPY() JOINT
    diff_ent_clients = []
    diff_ent_sessions = []

    for l in j_clients_only:
        diff_ent = st.differential_entropy(l[1])
        diff_ent_clients.append(diff_ent)
    for l in j_sessions:
        diff_ent = st.differential_entropy(l[1])
        diff_ent_sessions.append(diff_ent)

    data['Differential_Entropy_joint'].extend(diff_ent_clients)
    data['Differential_Entropy_joint'].extend(diff_ent_sessions)

    # plotGraph(diff_ent_clients,diff_ent_sessions,'Differential_Entropy_Joint')
    fout.write('|')

    # MEDIAN() FETCH
    median_clients = []
    median_sessions = []

    for l in f_clients_only:
        median = statistics.median(l[1])
        median_clients.append(median)
    for l in f_sessions:
        median = statistics.median(l[1])
        median_sessions.append(median)
    
    data['Median_fetch'].extend(median_clients)
    data['Median_fetch'].extend(median_sessions)

    fout.write('\n# Median\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(median_clients,median_sessions,'Median_Fetch')
    fout.write('|')

    # MEDIAN() REPLY
    median_clients = []
    median_sessions = []

    for l in r_clients_only:
        median = statistics.median(l[1])
        median_clients.append(median)
    for l in r_sessions:
        median = statistics.median(l[1])
        median_sessions.append(median)

    data['Median_reply'].extend(median_clients)
    data['Median_reply'].extend(median_sessions)
    
    # plotGraph(median_clients,median_sessions,'Median_Reply')
    fout.write('|')

    # MEDIAN() JOINT
    median_clients = []
    median_sessions = []

    for l in j_clients_only:
        median = statistics.median(l[1])
        median_clients.append(median)
    for l in j_sessions:
        median = statistics.median(l[1])
        median_sessions.append(median)

    data['Median_joint'].extend(median_clients)
    data['Median_joint'].extend(median_sessions)
    
    # plotGraph(median_clients,median_sessions,'Median_Joint')
    fout.write('|')

    # MEDIAN_ABS_DEVIATION() FETCH
    m_abs_dev_clients = []
    m_abs_dev_sessions = []

    for l in f_clients_only:
        m_abs_dev = st.median_abs_deviation(l[1])
        m_abs_dev_clients.append(m_abs_dev)
    for l in f_sessions:
        m_abs_dev = st.median_abs_deviation(l[1])
        m_abs_dev_sessions.append(m_abs_dev)
    
    data['Median_Absolute_Deviation_fetch'].extend(m_abs_dev_clients)
    data['Median_Absolute_Deviation_fetch'].extend(m_abs_dev_sessions)

    fout.write('\n# Median Absolute Deviation\n')
    fout.write('|Fetch|Reply|\n|-|-|\n')
    # plotGraph(m_abs_dev_clients,m_abs_dev_sessions,'Median_Absolute_Deviation_Fetch')
    fout.write('|')

    # MEDIAN_ABS_DEVIATION() REPLY
    m_abs_dev_clients = []
    m_abs_dev_sessions = []

    for l in r_clients_only:
        m_abs_dev = st.median_abs_deviation(l[1])
        m_abs_dev_clients.append(m_abs_dev)
    for l in r_sessions:
        m_abs_dev = st.median_abs_deviation(l[1])
        m_abs_dev_sessions.append(m_abs_dev)

    data['Median_Absolute_Deviation_reply'].extend(m_abs_dev_clients)
    data['Median_Absolute_Deviation_reply'].extend(m_abs_dev_sessions)

    # plotGraph(m_abs_dev_clients,m_abs_dev_sessions,'Median_Absolute_Deviation_Reply')
    fout.write('|')

    # MEDIAN_ABS_DEVIATION() JOINT
    m_abs_dev_clients = []
    m_abs_dev_sessions = []

    for l in j_clients_only:
        m_abs_dev = st.median_abs_deviation(l[1])
        m_abs_dev_clients.append(m_abs_dev)
    for l in j_sessions:
        m_abs_dev = st.median_abs_deviation(l[1])
        m_abs_dev_sessions.append(m_abs_dev)

    data['Median_Absolute_Deviation_joint'].extend(m_abs_dev_clients)
    data['Median_Absolute_Deviation_joint'].extend(m_abs_dev_sessions)

    # plotGraph(m_abs_dev_clients,m_abs_dev_sessions,'Median_Absolute_Deviation_Joint')
    fout.write('|')

    df_all = pd.DataFrame.from_dict(data)

    fAll = open('Mega_w_timeouts/stats/stats_all.csv','w')
    df_all.to_csv(fAll, index=False)
    fAll.close()

    return

def plotGraph(list_clients, list_sessions, name):
    plt.figure()
    if re.search('Min_Max',name) != None:
        typ = []
        group = []
        value = []

        for t in list_clients:
            typ.extend(['Min','Max'])
            group.extend(['clients','clients'])
            value.extend([t[0],t[1]])
        
        for t in list_sessions:
            typ.extend(['Min','Max'])
            group.extend(['probing','probing'])
            value.extend([t[0],t[1]])
        
        df = pd.DataFrame.from_dict(data = dict(types=typ, groups=group, values=value), orient='index',).T
        ax = splot(x=df['groups'], y=df['values'], hue=df['types'],data=df)

    elif re.search('Bayesian',name) != None:
        typ = []
        group = []
        value = []

        for t in list_clients:
            typ.extend(['Center','Lower','Upper'])
            group.extend(['clients','clients','clients'])
            value.extend([t[0],t[1][0],t[1][1]])
        
        for t in list_sessions:
            typ.extend(['Center','Lower','Upper'])
            group.extend(['probing','probing','probing'])
            value.extend([t[0],t[1][0],t[1][1]])
        
        df = pd.DataFrame.from_dict(data = dict(types=typ, groups=group, values=value), orient='index',).T
        ax = splot(x=df['groups'], y=df['values'], hue=df['types'],data=df)

    else:
        df = pd.DataFrame.from_dict(data = dict(clients=list_clients,probing = list_sessions), orient='index',).T
        ax = splot(data=df)

    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.title(name)
    plt.gcf().set_size_inches(12,9)
    figname = outdir+name+'.png'
    #plt.savefig(figname, format='png',dpi=300)
    #plt.show()

    fout.write('!['+name+']('+figname+')')
    return

def removeOutliers(lists):
    for l in lists:
        deleted = 0
        p25, p75 = np.percentile(l[1],q=[25,75])
        iqr = p75 - p25
        max =  p75 + 1.5*iqr
        min =  p25 - 1.5*iqr
        for value in l[1]:
            if value < min or value > max: 
                l[1].remove(value)
                deleted += 1
        if len(l[1]) < 2: 
            lists.remove(l)
    return

if __name__ == '__main__':

    fetch_file = 'Mega_w_timeouts/acceleration_fetch.pickle'
    reply_file = 'Mega_w_timeouts/acceleration_reply.pickle'
    joint_file = 'Mega_w_timeouts/acceleration_joint.pickle'
    cut = 2.5
    s_dir = 'Mega_w_timeouts/probes/merged_sessions/'
    fetch_out = 'Mega_w_timeouts/separated_acceleration_fetch'
    reply_out = 'Mega_w_timeouts/separated_acceleration_reply'
    joint_out = 'Mega_w_timeouts/separated_acceleration_joint'
    pattern = [1, 2, 4, 8, 12]
    outdir = 'Mega_w_timeouts/stats/'
    outfile = 'Mega_w_timeouts/stats/stats.md'

    f_clients_only, f_sessions = sa.separate(fetch_file, cut, s_dir, fetch_out, pattern)
    r_clients_only, r_sessions = sa.separate(reply_file, cut, s_dir, reply_out, pattern)
    j_clients_only, j_sessions = sa.separate(joint_file, cut, s_dir, joint_out, pattern)

    removeOutliers(f_clients_only)
    removeOutliers(f_sessions)
    removeOutliers(r_clients_only)
    removeOutliers(r_sessions)
    removeOutliers(j_clients_only)
    removeOutliers(j_sessions)

    print('f_clients_only: '+str(len(f_clients_only)))
    print('f_sessions: '+str(len(f_sessions)))
    print('r_clients_only: '+str(len(r_clients_only)))
    print('r_sessions: '+str(len(r_sessions)))
    print('j_clients_only: '+str(len(j_clients_only)))
    print('j_sessions: '+str(len(j_sessions)))

    fout = open(outfile,'wt')
    calcStats()
    fout.close()