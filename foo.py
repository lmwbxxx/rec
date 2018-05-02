from util import *

user_anchor_pair={}

anchors = set(load_pickle_file(path='../huajiao/anchor_sample'))
users = set(load_pickle_file(path='../huajiao/user_sample'))


def load_daily(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        attr = line.strip('\n').split()
        user_id = attr[0]
        anchor_id = attr[1]
        watching_duration = float(attr[3])
        if user_id in users and anchor_id in anchors:
            if user_id not in user_anchor_pair:
                user_anchor_pair[user_id] = {}
                user_anchor_pair[user_id][anchor_id]=watching_duration
            elif anchor_id not in user_anchor_pair[user_id]:
                user_anchor_pair[user_id][anchor_id]=watching_duration
            else:
                user_anchor_pair[user_id][anchor_id]+=watching_duration



def repeat_load():
    for i in range(0, 3, 1):
        filename = '../huajiao/daily/2017122' + str(i) + '/000000_0'
        load_daily(filename)

repeat_load()
pre={}
print 'ggg'
for user in user_anchor_pair:
    w=user_anchor_pair[user]
    w2 = sorted(w, key=w.get, reverse=True)
    if len(w2)>10:
        w2=w2[:10]
    pre[user]=w2


with open('../huajiao/pair34', 'rb') as h2:
    pair = pickle.load(h2)
tr={}
for usid, anid in pair:
    if usid not in users or anid not in anchors: continue
    if usid  in tr:
        tr[usid].add(anid)
    else:
        tr[usid]=set(anid)

z=0.0
s=0
for i in pre:
    s+=1
    if i in tr:
        if pre[i][0] in tr[i]: z+=1
print z/s,z,s