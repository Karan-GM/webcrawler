import pickle

def load_pickle(filename):
    file = open(filename, 'rb')
    dict_object = pickle.load(file)
    file.close()
    return(dict_object)

def run():
    inlink_dict = load_pickle("pickle/inlinks.pickle")
    outlink_dict = load_pickle("pickle/outlinks.pickle")

    print("Inlinks")
    for k, v in inlink_dict.items():
        print(k, v)

    print("Outlinks")
    for k, v in outlink_dict.items():
        print(k, v)