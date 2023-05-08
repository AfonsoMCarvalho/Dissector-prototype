import matplotlib.pyplot as plt

x = ['1/4','1/2','1','2','3']
fig,(tp,fp) = plt.subplots(2,3,sharex=True,figsize=(12,5))

tp[0].set(ylabel='True Positive Rate (%)')
tp[0].set_ylim(75,100)
tp[0].set_title('Reply stream')
tp[0].spines['right'].set_visible(False)
tp[0].spines['top'].set_visible(False)
tp[0].plot(x,[80,90,90,94,98],label='C4.5')
tp[0].plot(x,[92,94,90,98,98],label='Naive Bayes')
tp[0].plot(x,[84,92,88,96,98],label='Random Forrest')

fp[0].set(ylabel='False Positive Rate (%)')#,xlabel='Probe/Client ratio')
fp[0].set_ylim(0,4)
fp[0].spines['right'].set_visible(False)
fp[0].spines['top'].set_visible(False)
fp[0].plot(x,[2.8,1.2,1.2,0.4,0.4],label='C4.5')
fp[0].plot(x,[2.4,2.4,2.4,2,2],label='Naive Bayes')
fp[0].plot(x,[1.2,0.8,0.8,0.4,0.4],label='Random Forrest')
#=============================
# tp[1].set(ylabel='True Positive Rate (%)')
tp[1].set_ylim(75,100)
tp[1].set_title('Fetch stream')
tp[1].spines['right'].set_visible(False)
tp[1].spines['top'].set_visible(False)
tp[1].plot(x,[76,90,80,92,98],label='C4.5')
tp[1].plot(x,[80,80,86,96,98],label='Naive Bayes')
tp[1].plot(x,[78,80,84,98,96],label='Random Forrest')

fp[1].set(xlabel='Probe/Client ratio')#,ylabel='False Positive Rate (%)')
fp[1].set_ylim(0,4)
fp[1].spines['right'].set_visible(False)
fp[1].spines['top'].set_visible(False)
fp[1].plot(x,[1.6,4,2.4,1.2,0.4],label='C4.5')
fp[1].plot(x,[2.4,2.4,2,1.6,1.2],label='Naive Bayes')
fp[1].plot(x,[1.2,1.2,0.8,1.2,0.4],label='Random Forrest')
#=============================
# tp[2].set(ylabel='True Positive Rate (%)')
tp[2].set_ylim(75,100)
tp[2].set_title('Joint stream')
tp[2].spines['right'].set_visible(False)
tp[2].spines['top'].set_visible(False)
tp[2].plot(x,[82,80,88,94,98],label='C4.5')
tp[2].plot(x,[84,94,90,98,98],label='Naive Bayes')
tp[2].plot(x,[82,84,86,94,98],label='Random Forrest')

# fp[2].set(ylabel='False Positive Rate (%)',xlabel='Probe/Client ratio')
fp[2].set_ylim(0,4)
fp[2].spines['right'].set_visible(False)
fp[2].spines['top'].set_visible(False)
fp[2].plot(x,[2,2.4,1.6,0.8,0.4],label='C4.5')
fp[2].plot(x,[2,1.6,1.6,1.6,1.2],label='Naive Bayes')
fp[2].plot(x,[1.6,1.6,0.8,0.8,0],label='Random Forrest')

fp[1].legend(loc='lower center',ncol=3,bbox_to_anchor=(0.5,-0.5))

plt.subplots_adjust(top=0.945,bottom=0.175,right=0.985,left=0.055)

plt.savefig('/home/afonso/Documents/Class_all.pdf',format='pdf')
plt.show()

# REPLY
# [80,90,90,94,98]
# [92,94,90,98,98]
# [84,92,88,96,98]
# [2.8,1.2,1.2,0.4,0.4]
# [2.4,2.4,2.4,2,2]
# [1.2,0.8,0.8,0.4,0.4]
# FETCH
# [76,90,80,92,98]
# [80,80,86,96,98]
# [78,80,84,98,96]
# [1.6,4,2.4,1.2,0.4]
# [2.4,2.4,2,1.6,1.2]
# [1.2,1.2,0.8,1.2,0.4]
# JOINT
# [82,80,88,94,98]
# [84,94,90,98,98]
# [82,84,86,94,98]
# [2,2.4,1.6,0.8,0.4]
# [2,1.6,1.6,1.6,1.2]
# [1.6,1.6,0.8,0.8,0]