import random, pickle, pdb

anchor_attr = {}

with open('../huajiao/anchor_sample', 'rb') as h2:
    anchors = set(pickle.load(h2))
with open('../huajiao/user_sample', 'rb') as h2:
    users = set(pickle.load(h2))


def load_anchor_portrait(filename="../huajiao/anchor_portrait_20171225"):
    f = open(filename, 'r')
    lines = f.readlines()
    print len(lines)
    for line in lines:
        attr = line.strip('\n').split()  # bugs tab in ele
        anchor_id = attr[0]
        anchor_cap = int(attr[8])  # total watcher
        anchor_attr[anchor_id] = anchor_cap


propensity = {}


def load_negative(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        attr = line.strip('\n').split()
        user_id = attr[0]
        anchor_id = attr[2]
        rec_times = int(attr[3])
        click_times = int(attr[4])
        watch_duration=int(attr[5])
        if user_id in users and anchor_id in anchors:
            c = (user_id, anchor_id)
            if c not in propensity:
                propensity[c] = [rec_times, click_times, watch_duration]
            else:
                propensity[c][0] += rec_times
                propensity[c][1] += click_times
                propensity[c][2] += watch_duration


pair = {}


def load_daily(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        attr = line.strip('\n').split()
        user_id = attr[0]
        anchor_id = attr[1]
        watching_duration = float(attr[3])
        if user_id in users and anchor_id in anchors:
            c = (user_id, anchor_id)
            if c not in pair:
                pair[c] = watching_duration

                # pdb.set_trace()
            else:
                pair[c] += watching_duration


def samples(filename='../huajiao/daily/20171222/000000_0', usernum=10000, anchornum=1000):
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
    user_sample = random.sample(user_s, usernum)
    anchor_sample = random.sample(anchor_s, anchornum)
    with open('../huajiao/user_sample', 'wb') as h1:
        pickle.dump(user_sample, h1)
    with open('../huajiao/anchor_sample', 'wb') as h2:
        pickle.dump(user_sample, h2)


def save710():
    for i in range(7, 10, 1):
        print i
        filename = '../huajiao/daily/2017122' + str(i) + '/000000_0'
        load_daily(filename)
    print len(pair)
    with open('../huajiao/7-3/pair2', 'wb') as h:
        pickle.dump(pair, h, protocol=pickle.HIGHEST_PROTOCOL)

    for i in range(7, 10, 1):
        print i
        filename = '../huajiao/negative/negative_2017122' + str(i) + '.csv'
        load_negative(filename)
    print len(propensity)
    with open('../huajiao/7-3/prop2', 'wb') as h:
        pickle.dump(propensity, h, protocol=pickle.HIGHEST_PROTOCOL)

def save07():
    for i in range(0, 7, 1):
        print i
        filename = '../huajiao/daily/2017122' + str(i) + '/000000_0'
        load_daily(filename)
    print len(pair)
    with open('../huajiao/7-3/pair', 'wb') as h:
        pickle.dump(pair, h, protocol=pickle.HIGHEST_PROTOCOL)

    for i in range(0, 7, 1):
        print i
        filename = '../huajiao/negative/negative_2017122' + str(i) + '.csv'
        load_negative(filename)
    print len(propensity)
    with open('../huajiao/7-3/prop', 'wb') as h:
        pickle.dump(propensity, h, protocol=pickle.HIGHEST_PROTOCOL)

def save33():
    # for i in range(0, 3, 1):
    #     print i
    #     filename = '../huajiao/daily/2017122' + str(i) + '/000000_0'
    #     load_daily(filename)
    # print len(pair)
    # with open('../huajiao/pair03', 'wb') as h:
    #     pickle.dump(pair, h, protocol=pickle.HIGHEST_PROTOCOL)
    #
    # for i in range(6, 9, 1):
    #     print i
    #     filename = '../huajiao/negative/negative_2017122' + str(i) + '.csv'
    #     load_negative(filename)
    # print len(propensity)
    # with open('../huajiao/3-3/prop69', 'wb') as h:
    #     pickle.dump(propensity, h, protocol=pickle.HIGHEST_PROTOCOL)
    #
    for i in range(3, 4, 1):
        print i
        filename = '../huajiao/daily/2017122' + str(i) + '/000000_0'
        load_daily(filename)
    print len(pair)
    with open('../huajiao/pair34', 'wb') as h:
        pickle.dump(pair, h, protocol=pickle.HIGHEST_PROTOCOL)

    # for i in range(3, 6, 1):
    #     print i
    #     filename = '../huajiao/negative/negative_2017122' + str(i) + '.csv'
    #     load_negative(filename)
    # print len(propensity)
    # with open('../huajiao/prop36', 'wb') as h:
    #     pickle.dump(propensity, h, protocol=pickle.HIGHEST_PROTOCOL)

save33()