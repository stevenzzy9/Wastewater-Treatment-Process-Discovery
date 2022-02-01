
#read log file
fp=open('./log6.xes')
lines = fp.readlines()
#init parameters
count=0
#idx for <trace> and </trace> in log
idx=[]
#idx_jump for filter use
idx_jump=[]
#number for filter number of event
n=1
#start
for i in range(len(lines)):
    if'<trace>' in lines[i]:
        count=0
        idx.append(i)
        print('trace start line',i)
        idx_jump.append(i)
    if'<event>' in lines[i]:
        count=count+1
    if'</trace>' in lines[i]:
        if count>=n:
            idx.append(i)
            print('event in this trace is',count)
            print('trace end line',i)
            idx_jump.pop()
        else:
            idx.pop()
            idx_jump.append(i)
#print lines
i=0
for i in idx:
    print('trace in line',i)
for i in idx_jump:
    print('jump from line',i)
idx_jump.append(len(lines))
idx_jump.append(len(lines))
print('trace number is ',len(idx)/2)
#new_line is used for filtered log
new_line =[]
j=0
# if the line between the jump line, do not copy them
for i in range(len(lines)):
    if i<idx_jump[j]:
        new_line.append(lines[i])
    if i==idx_jump[j+1]:
        j=j+2
print(len(lines))
print(len(new_line))

#write to file
file=open('test.xes','w')
for i in range(len(new_line)):
    file.write(new_line[i]);
file.close()