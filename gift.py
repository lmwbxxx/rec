from datetime import date
gift=set()
def load(i):
    filename="../huajiao/gift/2017122"+str(i)+"/000000_0"
    f=open(filename,'r')
    lines=f.readlines()

    for line in lines:
        mess=line.strip('\n').split()
        time,_,usrid,anid=mess[0:4]
        money=round(float(mess[9]),2)
        if money !=0:
            gift.add((i,usrid,anid,money))

for i in range(10):
    load(i)
    print i

receive={}
for item in gift:
    i,usrid,anid,money=item
    if anid in receive:
        receive[anid][i]+=money
    else:
        receive[anid]=[0]*10
        receive[anid][i]=money
print len(receive)
for i in receive:
    sums=sum(receive[i])
    if sums>5000:print(receive[i])