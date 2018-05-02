import random
from util import *
from nmf import bpr,cbpr
import numpy as np
from bidict import bidict
order_list=load_pickle_file('../huajiao/bpr/order_list300')

def topK(K):
    tp=0
    fp=0
    tf=0
    topk=indice[:,-K:]
    tp={}
    ir={}
    for usid,anid in pair:
        if usid not in user2num or anid not in anchor2num: continue
        if usid not in tp: tp[usid]=0
        if usid not in ir: ir[usid]=0
        ir[usid]+=1
        usnum=user2num[usid]
        annum=anchor2num[anid]
        if annum in set(topk[usnum]):
            tp[usid]+=1
    precision=0
    recall=0
    count=0
    for uid in ir:
        count+=1
        precision+=(float(tp[uid])/K)
        recall+=(float(tp[uid])/ir[uid])
    precision/=count
    recall/=count
    return precision,recall

def topapK(K):
    ir={}
    for usid, anid in pair:
        if usid not in user2num or anid not in anchor2num: continue
        if usid not in ir: ir[usid]=0
        ir[usid]+=1

    apk={}
    for i in range(K):
        topk = indice[:,-i-1]
        for j in range(len(topk)):
            uid=user2num.inv[j]
            anid=anchor2num.inv[topk[j]]
            if (uid,anid) in pair:
                if uid in apk:
                    apk[uid].append(i)
                else:
                    apk[uid]=[i]
    apall=0.0
    for id in apk:
        hit=apk[id]
        ap=0.0
        for ind in hit:
            ap+=float(hit.index(ind)+1)/(ind+1)
        ap/=min(ir[id],K)
        apall+=ap
    apall/=M
    print len(apk)
    return apall










uij=set()
userset=set()
anchorset=set()
for pair in order_list:
    for j in order_list[pair]:
        uij.add((pair[0],pair[1],j))
        if pair[0] not in userset:
            userset.add(pair[0])
        if pair[1] not in anchorset:
            anchorset.add(pair[1])
        if j not in anchorset:
            anchorset.add(j)

user2num=bidict()
anchor2num=bidict()
for i in userset:
    user2num[i]=len(user2num)
for i in anchorset:
    anchor2num[i]=len(anchor2num)


S=[(user2num[u],anchor2num[i],anchor2num[j]) for (u,i,j) in uij]
M=len(user2num)
N=len(anchor2num)
userp=[0.5]*M
cap=[5]*N
#rat=bpr(S,M,N,K=10,steps=10)
rat=cbpr(S,M,N,cap=cap,userp=userp,K=10,steps=10)

with open('../huajiao/pair34', 'rb') as h2:
    pair = pickle.load(h2)

# for u,a in pair:
#     if u not in user2num or a not in anchor2num: continue
#     unum = user2num[u]
#     anum = anchor2num[a]
#     if rat[unum,anum]>1: print rat[unum,anum],pair[(u,a)]

indice=rat.argsort()

print topapK(1)
print topapK(5)
print topapK(10)
print topapK(20)
print topapK(50)
print topapK(100)
print '==============='


