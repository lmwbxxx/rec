import pickle
#import sklearn
from nmf import *
import numpy as np
import pdb
with open('../huajiao/pair03', 'rb') as h:
    mat = pickle.load(h)
with open('../huajiao/pair34', 'rb') as h2:
    test = pickle.load(h2)




user_dict={}
an_dict={}
for i in mat:
    useid=i[0]
    anchorid=i[1]
    if useid not in user_dict:
        user_dict[useid]=len(user_dict)
    if anchorid not in an_dict:
        an_dict[anchorid]=len(an_dict)
ratmatrix = np.zeros((len(user_dict), len(an_dict)))

for i in mat:
    ratmatrix[user_dict[i[0]]][an_dict[i[1]]]=np.log10(mat[i]+1)

print np.count_nonzero(ratmatrix)




ratmatrix=np.round(ratmatrix,2)
# predict=cmf(ratmatrix,cap,usep,K=10,steps=2)
#
P,Q=mf(ratmatrix,steps=5,K=10)
predict=numpy.dot(P,Q)

indice=predict.argsort()
def topK(K):
    tp=0
    fp=0
    tf=0
    topk=indice[:,-K:]
    tp={}
    ir={}
    for usid,anid in test:
        if usid not in user_dict or anid not in an_dict: continue
        if usid not in tp: tp[usid]=0
        if usid not in ir: ir[usid]=0
        ir[usid]+=1
        usnum=user_dict[usid]
        annum=an_dict[anid]
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

print topK(5)
print topK(10)
print topK(20)
print topK(50)
print topK(100)


# recommend=set()
# for row in xrange(len(predict)):
#     for column in xrange(len(predict[0])):
#         if ratmatrix[row][column]==0:
#             #if predict[row][column]>np.percentile(predict[:][row],95):
#             recommend.add((row,column))
#
# print(len(recommend))

# z=0
# # print len(prop)
# for i in prop2:
#     if i[0] not in user_dict or i[1] not in an_dict: continue
#     uid=user_dict[i[0]]
#     anid=an_dict[i[1]]
#     if ratmatrix[uid][anid]>2.5:
#         z+=1
#         print ratmatrix[uid][anid],prop2[i]
# print z

