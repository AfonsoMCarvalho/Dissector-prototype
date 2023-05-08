import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

nus = []
for n in range(0,100,5):
    nus.append(n / 100)

tols = []
for i in range(1,10):
    a = 10**i
    tols.append(1/a)

print(tols)

# fig,(tp,fp) = plt.subplots(2,3,sharex=True,figsize=(12,5))
fig,(tp,fp) = plt.subplots(2,1,sharex=True,figsize=(8,5))

for i in ['joint']:#,'fetch','joint']:
    mx,mn = None, None

    t = ''
    p = None
    if i == 'reply': 
        t = 'Reply Stream'
        p = 0
    elif i =='fetch': 
        t = 'Fetch Stream'
        p = 1
    elif i =='joint': 
        t = 'Joint Stream'
        p = 2

    if p == 2:
        # tp[p].set(ylabel='True Positive Rate (%)')
        # fp[p].set(ylabel='False Positive Rate (%)')
        tp.set(ylabel='True Positive Rate (%)')
        fp.set(ylabel='False Positive Rate (%)')
        fp.set(xlabel='Nu')
    # elif p == 1:
        # fp[p].set(xlabel='Nu')

    # tp[p].set_title(t)
    # tp[p].set_ylim(47,100)
    # tp[p].spines['right'].set_visible(False)
    # tp[p].spines['top'].set_visible(False)

    # fp[p].set_ylim(5,100)
    # fp[p].spines['right'].set_visible(False)
    # fp[p].spines['top'].set_visible(False)

    #tp.set_title(t)
    tp.set_ylim(85,95)
    tp.spines['right'].set_visible(False)
    tp.spines['top'].set_visible(False)

    fp.set_ylim(50,60)
    fp.spines['right'].set_visible(False)
    fp.spines['top'].set_visible(False)

    x = tols
    # tp[p].set_xscale('linear')
    tp.set_xscale('log')

    l = ''

    for j in [1,2,4,8,12]:
        if j == 1: l = 'PCR = 1/4'
        elif j == 2: l = 'PCR = 1/2'
        elif j == 4: l = 'PCR = 1'
        elif j == 8: l = 'PCR = 2'
        elif j == 12: l = 'PCR = 3'
        print(f'{i} - {j} probes:')
        tps = []
        fps = []
        for param in tols:
            df = pd.read_csv(f'Mega_w_timeouts/stats/anomaly_detection/rbf/{i}_{j}probes_no_scaling_rbf.csv')
            df2 = df.loc[(df['gamma']=='scale') & (df['tolerance']==param) & (df['nu']==0.5)]
            #print(df2)
            value = df2['test_accuracy_%'].values
            if len(value) == 0: tps.extend([None])
            else: tps.extend(value)

            value = 100-df2['validation_accuracy_%'].values
            if len(value) == 0: fps.extend([None])
            else: fps.extend(value)

        for z in range(len(tps)):
            if tps[z] == -1 or fps[z] == -1:
                tps[z] = None
                fps[z] = None

        # if p == 2:
            # tp[p].plot(x,tps,label=l)
            # fp[p].plot(x,fps,label='All PCR',color='brown')
        tp.plot(x,tps,label=l)
        fp.plot(x,fps,label='All PCR',color='brown')
        # else:
            # tp[p].plot(x,tps)
            # fp[p].plot(x,fps,color='brown')

        handles, labels = [],[]
        # h, la = tp[p].get_legend_handles_labels()
        h, la = tp.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(la)
        # h, la = fp[p].get_legend_handles_labels()
        h, la = fp.get_legend_handles_labels()
        if h != [] and la != []:
            handles.append(h[0])
            labels.append(la[0])

    fig.legend(handles,labels,loc='lower center',ncol=6)#,bbox_to_anchor=(0.5,1.35))
    # plt.subplots_adjust(top=0.940,bottom=0.170,right=0.990,left=0.055)
    plt.subplots_adjust(top=0.955,bottom=0.170,right=0.970,left=0.095)
plt.savefig('/home/afonso/Documents/AD_tol_Joint.pdf',format='pdf')
plt.show()