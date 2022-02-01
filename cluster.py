
import numpy as np
from scipy.cluster.vq import vq,kmeans,whiten
event = ["invite reviewers","get review 1","get review 2","get review 3","time-out 1","time-out 2","time-out 3",
        "collect reviews","decide","get review X","time-out X","invite additional reviewer","accept","reject",]

#read log file
fp=open('./log/review_example_large.xes')
lines = fp.readlines()

idx=[]

for i in range(len(lines)):
    if'<trace>' in lines[i]:
        idx.append(i)
        #print("trace start line ",i)
    if '</trace>' in lines[i]:
        idx.append(i)
        #print("trace end line ", i)
print(len(idx))
vector_space = []
for i in range(len(idx)):
    if i== 19999:
        break
    start = idx[i]
    end = idx[i+1]
    j = start
    array = np.zeros(14)
    for j in range(start,end):
        for k in range(len(event)):
            if event[k] in lines[j]:
                array[k]=array[k]+1
    if (np.all(array==0))==0:
        #print(array)
        vector_space.append(array)
    i=i+2

centroids,_=kmeans(vector_space,6)

result,_=vq(vector_space,centroids)
print(result)

log1=[]
log2=[]
log3=[]
log4=[]
log5=[]
log6=[]
head='<log xes.version="1.0" xes.features="nested-attributes" openxes.version="1.0RC7" xmlns="http://www.xes-standard.org/">'
bottom = '</log>'
for i in range(len(result)):
    start = idx[2*i]
    end = idx[2*i+1]
    if result[i]==0:
        for j in range(start, end):
            log1.append(lines[j])
        log1.append(lines[j+1])
    if result[i]==1:
        for j in range(start, end):
            log2.append(lines[j])
        log2.append(lines[j + 1])
    if result[i]==2:
        for j in range(start, end):
            log3.append(lines[j])
        log3.append(lines[j+1])
    if result[i]==3:
        for j in range(start, end):
            log4.append(lines[j])
        log4.append(lines[j + 1])
    if result[i]==4:
        for j in range(start, end):
            log5.append(lines[j])
        log5.append(lines[j+1])
    if result[i]==5:
        for j in range(start, end):
            log6.append(lines[j])
        log6.append(lines[j + 1])
#write to file
file=open('log1.xes','w')
for i in range(len(log1)):
    file.write(log1[i]);
file.close()

#write to file
file=open('log2.xes','w')
for i in range(len(log2)):
    file.write(log2[i]);
file.close()

#write to file
file=open('log3.xes','w')
for i in range(len(log3)):
    file.write(log3[i]);
file.close()

#write to file
file=open('log4.xes','w')
for i in range(len(log4)):
    file.write(log4[i]);
file.close()

#write to file
file=open('log5.xes','w')
for i in range(len(log5)):
    file.write(log5[i]);
file.close()

#write to file
file=open('log6.xes','w')
for i in range(len(log6)):
    file.write(log6[i]);
file.close()