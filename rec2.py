import random
from util import *
from nmf import bpr,cbpr
import numpy as np
from bidict import bidict
order_list=load_pickle_file('../huajiao/bpr/order_new')
import pdb
# def topK(K):
#     tp=0
#     fp=0
#     tf=0
#     topk=indice[:,-K:]
#     tp={}
#     ir={}
#     for usid,anid in pair:
#         if usid not in user2num or anid not in anchor2num: continue
#         if usid not in tp: tp[usid]=0
#         if usid not in ir: ir[usid]=0
#         ir[usid]+=1
#         usnum=user2num[usid]
#         annum=anchor2num[anid]
#         if annum in set(topk[usnum]):
#             tp[usid]+=1
#     precision=0
#     recall=0
#     count=0
#     for uid in ir:
#         count+=1
#         precision+=(float(tp[uid])/K)
#         recall+=(float(tp[uid])/ir[uid])
#     precision/=count
#     recall/=count
#     return precision,recall

def topapK():
    ir={}
    for usid, anid in pair:
        if usid not in user2num or anid not in anchor2num: continue
        if usid not in ir: ir[usid]=0
        ir[usid]+=1

    apk={}
    for K in [1,5,10,20]:
        apk={}
        for i in range(K):
            topk = indice[:,-i-1]
            for j in range(len(topk)):
                uid=user2num.inv[j]
                anid=anchor2num.inv[topk[j]]
                if (uid,anid) in pair and float(pair[(uid,anid)])>180:
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
        print 'ap@', K,apall
    hitatk=[0]*100
    for id in apk:
        x=apk[id]
        for ind in x:
            hitatk[ind]+=1
    for i in [1,5,10,20]:
        print (sum(hitatk[:i])/float(i))/M
    for j in [1,5,10,20,50]:
        re=0
        for id in apk:
            x=apk[id]
            re+=float(len([i for i in x if i<j]))/ir[id]

        print re/M









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
    anchor2num[i]=len(anchor2num)# indice=rat.argsort()



S=[(user2num[u],anchor2num[i],anchor2num[j]) for (u,i,j) in uij]
M=len(user2num)
N=len(anchor2num)
userp=[0.5]*M
cap=[3]*N
rat=bpr(S,M,N,K=15,steps=5)
#rat = np.random.rand(M,N)

#rat=cbpr(S,M,N,cap=cap,userp=userp,K=10,steps=1)

with open('../huajiao/bpr/pair', 'rb') as h2:
    pair = pickle.load(h2)


indice=rat.argsort()













# for u,a in pair:
#     if u not in user2num or a not in anchor2num: continue
#     unum = user2num[u]
#     anum = anchor2num[a]
#     if rat[unum,anum]>1: print rat[unum,anum],pair[(u,a)]

# indice=rat.argsort()
#
topapK()


