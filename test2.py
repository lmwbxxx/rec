import pickle,pdb
import random
from util import *



class Makedata:
    def __init__(self):
        self.bpr = {}
        self.anchors = set(load_pickle_file(path='../huajiao/anchor_sample'))
        self.users = set(load_pickle_file(path='../huajiao/user_sample'))

    def bpr_sample(self,filename='../huajiao/daily/20171222/000000_0',usernum=10000,anchornum=3000):
        uidset=set()
        aidset=set()

        user_anchor_pair = {}
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            attr = line.strip('\n').split()
            user_id,anchor_id = attr[:2]
            watching_duration = float(attr[3])
            c = (user_id, anchor_id)
            if c not in user_anchor_pair:
                user_anchor_pair[c] = watching_duration
            else:
                user_anchor_pair[c] += watching_duration

        sorted_pair=sorted(user_anchor_pair,key=user_anchor_pair.get,reverse=True)
        #pdb.set_trace()
        for uid,aid in sorted_pair:
            if uid not in uidset and len(uidset) < usernum:
                uidset.add(uid)
            if aid not in aidset and len(aidset) < anchornum:
                aidset.add(aid)
        save_pickle_file(uidset,'../huajiao/user_sample')
        save_pickle_file(aidset,'../huajiao/anchor_sample')


    def load_daily(self, filename):
        user_anchor_pair = {}
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            attr = line.strip('\n').split()
            user_id = attr[0]
            anchor_id = attr[1]
            watching_duration = float(attr[3])
            if user_id in self.users and anchor_id in self.anchors:
                c = (user_id, anchor_id)
                if c not in user_anchor_pair:
                    user_anchor_pair[c] = watching_duration
                else:
                    user_anchor_pair[c] += watching_duration
        self.generate_order(user_anchor_pair)
        return user_anchor_pair

    def generate_order(self, user_anchor_pair):
        orders = {}
        for pair in user_anchor_pair:
            user_id = pair[0]
            anchor_id = pair[1]
            if user_id not in orders:
                orders[user_id] = []
                if user_anchor_pair[pair] > 600:
                    orders[user_id].append(anchor_id)
        for user_id in orders:
            for positive_anchor in orders[user_id]:
                pair = (user_id, positive_anchor)
                if pair not in self.bpr:
                    neg_sample = random.sample(self.anchors - set(orders[user_id]), 50)
                    self.bpr[pair] = neg_sample

    def repeat_load(self):
        for i in range(0, 3, 1):
            filename = '../huajiao/daily/2017122' + str(i) + '/000000_0'
            self.load_daily(filename)

    def load_negative(self, filename):
        propensity = {}
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            attr = line.strip('\n').split()
            user_id = attr[0]
            anchor_id = attr[2]
            rec_times = int(attr[3])
            click_times = int(attr[4])
            watch_duration = int(attr[5])
            if user_id in self.users and anchor_id in self.anchors:
                c = (user_id, anchor_id)
                if c not in propensity:
                    propensity[c] = [rec_times, click_times, watch_duration]
                else:
                    propensity[c][0] += rec_times
                    propensity[c][1] += click_times
                    propensity[c][2] += watch_duration

x=Makedata()
# x.bpr_sample()
x.repeat_load()
print len(x.bpr)
save_pickle_file(x.bpr,'../huajiao/bpr/order_list')