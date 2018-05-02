import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.neural_network import MLPClassifier
import numpy as np
import pdb

with open('../huajiao/feature', 'rb') as h:
    f1 = pickle.load(h)
with open('../huajiao/feature2', 'rb') as h2:
    f2 = pickle.load(h2)

value=f1.values()[0]
n_features=len(value)-2
n_samples=len(f1)

value2=f2.values()[0]
n_features2=len(value2)-2
n_samples2=len(f2)


y=np.zeros(shape=(n_samples,1))
x=np.zeros(shape=(n_samples,n_features))
y2=np.zeros(shape=(n_samples2,1))
x2=np.zeros(shape=(n_samples2,n_features2))
j=0
a=b=0
#pdb.set_trace()
for i in f1:
    fealist=f1[i]
    #pdb.set_trace()
    watch_time=fealist[-1]
    y[j]=1 if watch_time>60 else 0
    x[j]=fealist[:-2]
    j+=1
j=0
for i in f2:
    fealist=f2[i]
    watch_time=fealist[-1]
    y2[j]=1 if watch_time>60 else 0

    x2[j]=fealist[:-2]
    j+=1
model=svm.LinearSVC(class_weight='balanced')
model.fit(x,y)
#pdb.set_trace()
tp=0
fp=0
fn=0
for i in xrange(n_samples2):
    pre=model.predict(x2[i].reshape(1, -1))
    if y2[i]==1 and pre==1: tp+=1
    if y2[i]==1 and pre ==0: fn+=1
    if y2[i]==0 and pre ==1: fp+=1
precision=float(tp)/(tp+fp)
recall=float(tp)/(tp+fn)
f1=2*precision*recall/(precision+recall)
print tp
print "Accuracy is ", model.score(x2,y2)
print "Precision id ", precision
print "Recall is ", recall
print "F1 is ", f1












