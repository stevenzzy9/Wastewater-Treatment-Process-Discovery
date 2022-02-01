import numpy as np
from scipy.cluster.vq import vq,kmeans,whiten
event = ["invite reviewers","get review 1","get review 2","get review 3","time-out 1","time-out 2","time-out 3",
        "collect reviews","decide","get review X","time-out X","invite additional reviewer","accept","reject",]
dependency=["i1-g1","i1-g2","i1-g3","i1-t1","i1-t2","i1-t3","g1-c","g2-c","g3-c","t1-c","t2-c","t3-c","c-d",
            "d-a","d-i2","d-r","i2-gx","i2-tx","tx-i2","gx-i2","gx-a","gx-r"]
#read log file
fp=open('./log/review_example_large.xes')
lines = fp.readlines()

idx=[]
idx_event =[]
for i in range(len(lines)):
    if'<trace>' in lines[i]:
        idx.append(i)
        #print("trace start line ",i)
    if '</trace>' in lines[i]:
        idx.append(i)
        #print("trace end line ", i)
    if'<event>' in lines[i]:
        idx_event.append(i)
    if'</event>' in lines[i]:
        idx_event.append(i)
print(len(idx))
print(len(idx_event)/2)
vector_space = []
s=0
for i in range(len(idx)):
    if i== 19999:
        break
    start = idx[i]
    end = idx[i+1]
    j = start
    array = np.zeros(14)
    dep=np.zeros(22)
    time_dependency= 0
    last_event="invite reviewers"
    for j in range(start,end):
            for k in range(len(event)):
                if event[k] in lines[j]:
                    array[k]=array[k]+1
            if "complete" in lines[j]:
                if "time:timestamp" in lines[j-1]:
                    complete_time=lines[j - 1][42:47]
                    mm1=int(complete_time[0:2])
                    dd1=int(complete_time[3:5])
                    #print(lines[j - 1][42:47])
                    #time.append(lines[j - 1][42:47])
                elif "time:timestamp" in lines[j-2]:
                    complete_time = lines[j - 2][42:47]
                    mm1=int(complete_time[0:2])
                    dd1=int(complete_time[3:5])
                    #time.append(lines[j - 2][42:47])
                elif "time:timestamp" in lines[j+1]:
                    #time.append(lines[j + 1][42:47])
                    complete_time = lines[j + 1][42:47]
                    mm1=int(complete_time[0:2])
                    dd1=int(complete_time[3:5])
                if "concept:name" in lines[j-1]:
                    for k in range(len(event)):
                        if event[k] in lines[j-1]:
                            event_name= event[k]
                            #event_name.append(event[k])
                            #print(event_name)
                if "concept:name" in lines[j + 1]:
                    for k in range(len(event)):
                        if event[k] in lines[j + 1]:
                            event_name = event[k]
                            #event_name.append(event[k])
                if event_name=="invite reviewers":
                    time_dependency = complete_time
                    mm2=int(time_dependency[0:2])
                    dd2=int(time_dependency[3:5])
                if event_name=="get review 1":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    dep[0]=final_time
                if event_name=="get review 2":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    dep[1]=final_time
                if event_name=="get review 3":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    dep[2]=final_time
                if event_name=="time-out 1":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    dep[3]=final_time
                if event_name=="time-out 2":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    dep[4]=final_time
                if event_name=="time-out 3":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    dep[5]=final_time
                if event_name=="collect reviews":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    if last_event=="get review 1":
                        dep[6] = final_time
                    if last_event=="get review 2":
                        dep[7] = final_time
                    if last_event=="get review 3":
                        dep[8] = final_time
                    if last_event=="time out 1":
                        dep[9] = final_time
                    if last_event=="time out 2":
                        dep[10] = final_time
                    if last_event=="time out 3":
                        dep[11] = final_time
                if event_name=="decide":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    dep[12]=final_time
                if event_name == "invite additional reviewer":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    if final_time<0:
                        final_time+30
                    if last_event == "decide":
                        dep[14] = final_time
                    if last_event=="get review X":
                        dep[19]= final_time
                    if last_event == "time out X":
                        dep[18] = final_time
                if event_name == "time out X":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    dep[17] = final_time
                if event_name == "get review X":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    dep[16]= final_time
                if event_name=="accept":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    if last_event=="decide":
                        dep[13]=final_time
                    if last_event=="get review X":
                        dep[20]=final_time
                if event_name == "reject":
                    m=mm1-mm2
                    d=dd1-dd2
                    if m<0:
                        m=m+12
                    if d<0:
                        d=d+30
                        m=m-1
                    final_time=m*30+d
                    if last_event == "decide":
                        dep[15]=final_time
                    if last_event == "get review X":
                        dep[21]=final_time
                last_event=event_name
                time_dependency = complete_time
                mm2 = int(time_dependency[0:2])
                dd2 = int(time_dependency[3:5])
    if (np.all(array==0))==0:
        if (np.all(dep == 0)) == 0:
            #print(np.hstack((array,dep)))
            vector_space.append(np.hstack((array,dep)))
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
head='<log xes.version="1.0" xes.features="nested-attributes" openxes.version="1.0RC7" xmlns="http://www.xes-standard.org/">'+'\n'
tail = '</log>'
log1.append(head)
log2.append(head)
log3.append(head)
log4.append(head)
log5.append(head)
log6.append(head)
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

log1.append(tail)
log2.append(tail)
log3.append(tail)
log4.append(tail)
log5.append(tail)
log6.append(tail)
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