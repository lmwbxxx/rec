# for i in range(7,10,1):
#     print i
#     filename='../huajiao/negative/negative_2017122'+str(i)+'.csv'
#     load_negative(filename)
import random,pickle

propensity={}
def load_negative(filename='../huajiao/negative/negative_20171220.csv'):
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        attr = line.strip('\n').split()
        user_id=attr[0]
        anchor_id=attr[2]
        rec_times=int(attr[3])
        click_times=int(attr[4])
        watch_times=int(attr[5])
        c = (user_id, anchor_id)
        if c not in propensity:
            propensity[c]=[rec_times,click_times,watch_times]
        else:
            propensity[c][0]+=rec_times
            propensity[c][1]+=click_times
            propensity[c][2]+=watch_times
load_negative()
l=sorted(propensity,key=lambda x:propensity[x][1],reverse=True)

def samples(popul,filename='../huajiao/daily/20171222/000000_0',usernum=20000, anchornum=2000):
    f = open(filename, 'r')
    lines = f.readlines()
    pair = {}
    user_s = set()
    anchor_s = set()
    for line in lines:
        attr = line.strip('\n').split()
        user_id = attr[0]
        anchor_id = attr[1]
        if user_id not in user_s:
            user_s.add(user_id)
        if anchor_id not in anchor_s:
            anchor_s.add(anchor_id)
    user_sample = random.sample(user_s, usernum/2)
    anchor_sample = random.sample(anchor_s, anchornum/2)
    for i in popul:
        if len(user_sample) >usernum and len(anchor_sample) >anchornum: break
        elif len(user_sample)<= usernum and i[0] not in set(user_sample):
            user_sample.append(i[0])
        elif len(anchor_sample)<= anchornum and i[0] not in set(anchor_sample):
            anchor_sample.append(i[1])

    with open('../huajiao/user_sample','wb') as h1:
        pickle.dump(user_sample,h1)
    with open('../huajiao/anchor_sample','wb') as h2:
        pickle.dump(user_sample,h2)

samples(l)