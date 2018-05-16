from util import *
import logging,random,pdb

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: %(levelname)s: %(message)s", datefmt='%H:%M:%S'
)

user_set = load_pickle_file('../huajiao/user_sample_new')
anchor_set = load_pickle_file('../huajiao/anchor_sample_new')


class watch:
    def __init__(self):
        self.user_online = {}
        self.anchor_online = {}
        self.user_anchor_pair={}
        self.bpr={}

    def get_online_anchor(self, id):
        online_anchor_list=[]
        for i in anchor_set:
            if i in self.anchor_online:
                if self.anchor_online[i][0]<self.user_online[id][1] and self.user_online[id][0] < self.anchor_online[i][1]:
                    online_anchor_list.append(i)
        return online_anchor_list


    def load_file(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            sep = line.strip('\n').split()
            user_id, anchor_id, live_id, timestamp, watch_second = sep[:5]
            timestamp = int(timestamp)
            watch_second = float(watch_second)
            if user_id not in user_set or anchor_id not in anchor_set or watch_second==0:
                continue
            if (user_id,anchor_id) not in self.user_anchor_pair:
                self.user_anchor_pair[(user_id,anchor_id)]=watch_second
            else : self.user_anchor_pair[(user_id,anchor_id)]+=watch_second

            if user_id in self.user_online:
                self.user_online[user_id] = (min(timestamp, self.user_online[user_id][0]),
                                             max(timestamp + watch_second, self.user_online[user_id][1]))
            elif user_id not in self.user_online:
                self.user_online[user_id] = (timestamp, timestamp + watch_second)
            if anchor_id in self.anchor_online:
                self.anchor_online[anchor_id] = (min(timestamp, self.anchor_online[anchor_id][0]),
                                                 max(timestamp + watch_second, self.anchor_online[anchor_id][1]))
            elif anchor_id not in self.anchor_online:
                self.anchor_online[anchor_id] = (timestamp, timestamp + watch_second)

    def get_negaive_sample(self):
        orders = {}
        for pair in self.user_anchor_pair:
            user_id = pair[0]
            anchor_id = pair[1]
            if self.user_anchor_pair[pair] > 300:
                if user_id not in orders:
                    orders[user_id] = []
                orders[user_id].append(anchor_id)
        for user_id in orders:
            for positive_anchor in orders[user_id]:
                #pdb.set_trace()
                pair = (user_id, positive_anchor)
                if pair not in self.bpr:
                    aval_set=set(self.get_online_anchor(user_id)) - set(orders[user_id])
                    number=min(len(aval_set),50)
                    #pdb.set_trace()# indice=rat.argsort()

                    if len(aval_set)<50:
                        neg_sample=aval_set.union(set(random.sample(anchor_set-aval_set,50-len(aval_set))))
                    neg_sample = random.sample(aval_set, number)
                    self.bpr[pair] = neg_sample

o={}
def merge(a,b):

    for j in b:
        a[j]=b[j]
    return a

for i in range(0, 7, 1):
    print i
    x = watch()
    filename = '../huajiao/watch/2017122' + str(i) + '/000000_0'
    x.load_file(filename)
    x.get_negaive_sample()
    o=merge(o,x.bpr)

print len(o)
save_pickle_file(o,'../huajiao/bpr/order_new')


corres_online_anchor={}
y=watch()
filename = '../huajiao/watch/20171227/000000_0'
y.load_file(filename)
for user in user_set:
    if user in y.user_online:
        corres_online_anchor[user]=y.get_online_anchor(user)

save_pickle_file(corres_online_anchor,'../huajiao/bpr/online_anchor')
save_pickle_file(y.user_anchor_pair,'../huajiao/bpr/pair')
