from util import *
class Sample:
    def __init__(self,user_num,anchor_num):
        self.user_anchor_pair={}
        self.user_num=user_num
        self.anchor_num=anchor_num

    def sample(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            attr = line.strip('\n').split()
            user_id, anchor_id = attr[:2]
            watching_duration = float(attr[3])
            c = (user_id, anchor_id)
            if c not in self.user_anchor_pair:
                self.user_anchor_pair[c] = watching_duration
            else:
                self.user_anchor_pair[c] += watching_duration


    def generate_filename(self):
        for i in range(1, 5, 1):
            print i
            filename = '../huajiao/daily/2017122' + str(i) + '/000000_0'
            self.sample(filename)

    def sort(self):
        uidset = set()
        aidset = set()
        sorted_pair=sorted(self.user_anchor_pair,key=self.user_anchor_pair.get,reverse=True)
        for uid,aid in sorted_pair:
            if uid not in uidset and len(uidset) < usernum:
                uidset.add(uid)
            if aid not in aidset and len(aidset) < anchornum:
                aidset.add(aid)
        save_pickle_file(uidset,'../huajiao/user_sample')
        save_pickle_file(aidset,'../huajiao/anchor_sample')