import numpy as np
np.set_printoptions(suppress=True)
import datetime

def get_event_name(lines,start,end):
    find_all = lambda data, s: [r for r in range(len(data)) if data[r] == s]
    for i in range(start,end):
        if "concept:name" in lines[i]:
            r_list = find_all(lines[i], '"')
            event_name = lines[i][r_list[2]+1:r_list[3]]
    return  event_name

def get_event_time(lines,start,end):
    find_all = lambda data, s: [r for r in range(len(data)) if data[r] == s]
    for i in range(start,end):
        if "time:timestamp" in lines[i]:
            r_list = find_all(lines[i], '"')
            event_time = lines[i][r_list[2]+1:r_list[3]-15]
    event_time=datetime.datetime.strptime(event_time,"%Y-%m-%d")
    return  event_time

def get_full_event(lines):
    event=[]
    find_all = lambda data, s: [r for r in range(len(data)) if data[r] == s]
    for i in range(len(lines)):
        if "meta_concept:named_events_total" in lines[i]:
            start=i
            for j in range(i,len(lines)):
                if "</int>" in lines[j]:
                    end = j
                    break
    for i in range(start+1,end-1):
        r_list = find_all(lines[i], '"')
        event_name = lines[i][r_list[0] + 1:r_list[1]]
        event.append(event_name)
    return event

def get_full_dependency(lines,start_event):
    dependency=[]
    idx=[]
    idx_event=[]
    index_in_event = 0
    for i in range(len(lines)):
        if '<trace>' in lines[i]:
            idx.append(i)
            # print("trace start line ",i)
        if '</trace>' in lines[i]:
            idx.append(i)
        if '<event>' in lines[i]:
            idx_event.append(i)
        if '</event>' in lines[i]:
            idx_event.append(i)
    for i in range(0, len(idx), 2):
        if i == len(idx) - 1:
            break
        start = idx[i]
        end = idx[i + 1]
        j = start

        last_event = start_event
        event_in_trace = 0
        for j in range(start, end):
            if '<event>' in lines[j]:
                event_in_trace = event_in_trace + 1
        for k in range(0, event_in_trace):
            event_start = idx_event[index_in_event]
            event_end = idx_event[index_in_event + 1]
            event_name = get_event_name(lines, event_start, event_end)
            if event_name == start_event:
                event_name = start_event
            else:
                edge = last_event + '-' + event_name
                if edge not in dependency:
                    dependency.append(edge)
            last_event = event_name
            index_in_event = index_in_event + 2
    return dependency

def get_trace_index(lines):
    idx=[]
    for i in range(len(lines)):
        if '<trace>' in lines[i]:
            idx.append(i)
        if '</trace>' in lines[i]:
            idx.append(i)
    return  idx

def get_event_index(lines):
    idx=[]
    for i in range(len(lines)):
        if '<event>' in lines[i]:
            idx.append(i)
        if '</event>' in lines[i]:
            idx.append(i)
    return  idx

fp=open('./log/Road_Traffic_Fine_Management_Process.xes')
lines = fp.readlines()

event =get_full_event(lines)
print(len(event))
print(event)
dependency = get_full_dependency(lines,"Create Fine")
print(len(dependency))
print(dependency)