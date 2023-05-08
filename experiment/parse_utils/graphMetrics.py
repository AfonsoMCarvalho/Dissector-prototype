import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

fig,(f1,p4) = plt.subplots(1,2,figsize=(12,5))

x = ['1/4','1/2','1','2','3']
f1s = [['Supervised Learning',[0.902,0.939,0.918,0.970,0.990]],
       ['Anomaly Detection',  [0.850,0.869,0.853,0.891,0.926]]]

p4s = [['Supervised Learning',[0.939,0.963,0.950,0.982,0.994]],
       ['Anomaly Detection',  [0.792,0.812,0.792,0.850,0.895]]]

f1.set(ylabel='F1-score')
f1.set(xlabel='PCR')
p4.set(ylabel='P4')
p4.set(xlabel='PCR')

f1.set_ylim(0.75,1)
f1.spines['right'].set_visible(False)
f1.spines['top'].set_visible(False)

p4.set_ylim(0.75,1)
p4.spines['right'].set_visible(False)
p4.spines['top'].set_visible(False)

for i in f1s:
    f1.plot(x,i[1],label=i[0])

for i in p4s:
    p4.plot(x,i[1],label=i[0])

handles, labels = f1.get_legend_handles_labels()

fig.legend(handles,labels,loc='lower center',ncol=3)#,bbox_to_anchor=(0.5,1.35))
plt.subplots_adjust(top=0.950,bottom=0.140,right=0.985,left=0.070)
plt.savefig('/home/afonso/Documents/AD_vs_SupLearn.pdf',format='pdf')
plt.show()