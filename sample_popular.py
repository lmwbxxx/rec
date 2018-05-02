from util import *
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: %(levelname)s: %(message)s", datefmt='%H:%M:%S'
)

class Sample:
    def __init__(self, user_num, anchor_num):
        self.user_anchor_pair = {}
        self.user_num = user_num
        self.anchor_num = anchor_num
        self.uidset = set()
        self.aidset = set()

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
        for i in range(1, 4, 1):
            logging.info('%d',i)
            filename = '../huajiao/daily/2017122' + str(i) + '/000000_0'
            self.sample(filename)
        self.sort()
        self.save()

    def sort(self):
        sorted_pair = sorted(self.user_anchor_pair, key=self.user_anchor_pair.get, reverse=True)
        for uid, aid in sorted_pair:
            if uid not in self.uidset and len(self.uidset) < self.user_num:
                self.uidset.add(uid)
            if aid not in self.aidset and len(self.aidset) < self.anchor_num:
                self.aidset.add(aid)
            if len(self.uidset) >= self.user_num and len(self.aidset) >= self.anchor_num:
                break

    def save(self):
        logging.info('%d %d', len(self.uidset),len(self.aidset))

        save_pickle_file(self.uidset, '../huajiao/user_sample_new')
        save_pickle_file(self.aidset, '../huajiao/anchor_sample_new')

x=Sample(10000,3000)
x.generate_filename()