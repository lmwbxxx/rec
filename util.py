import pickle
def save_pickle_file(file, path):
    with open(path, 'wb') as h:
        pickle.dump(file, h, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle_file(path):
    with open(path, 'rb') as h:
        return pickle.load(h)
