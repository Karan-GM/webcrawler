import timeit
import pickle

class Summary():
    count = 0
    start_time = None
    end_time = None
    inlinks_dict = {}
    outlinks_dict = {}

    def set_start_time(self):
        self.start_time = timeit.default_timer()

    def set_end_time(self):
        self.end_time = timeit.default_timer()

    def get_count(self):
        return(self.count)

    ## Update Count
    def update_count(self):
        self.count = self.count + 1
        return(self.count)

    ## Updating Outlinks Dictionary
    # Key - Url
    # Values - All outlinks from that url
    def update_outlinks_dict(self, url, outlinks):
        ## Updating Outlink Dictionary
        if url in self.outlinks_dict:
            # print(url)
            # print(len(outlinks))
            # print(outlinks)
            print('Error, should not happen as de-duplication is enabled')
        else:
            self.outlinks_dict[url] = outlinks

    ## Updating Inlink dictionary
    # Key - Url
    # Values - All links of webpages pointing to that url
    def update_inlinks_dict(self, url, inlink):
        if url in self.inlinks_dict:
            self.inlinks_dict[url].append(inlink)
        else:
            self.inlinks_dict[url] = [inlink]

    def create_pickle_file(self, filename, dict_object):
        file_object = open(filename, 'wb')
        pickle.dump(dict_object, file_object, protocol=pickle.HIGHEST_PROTOCOL)
        file_object.close()

    def dump(self):
        print('Total number of documents crawled and scraped {}'.format(self.count))

        print('######### Start Time: {}'.format(self.start_time))
        print('######### End Time: {}'.format(self.end_time))
        total_time = self.end_time - self.start_time
        print('######### Total time took for crawling {}'.format(total_time))

        self.create_pickle_file("pickle/inlinks.pickle", self.inlinks_dict)
        self.create_pickle_file("pickle/outlinks.pickle", self.outlinks_dict)
