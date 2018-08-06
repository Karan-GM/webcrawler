from nltk.stem.porter import PorterStemmer
import re

class Keywords():
    keywords = None

    pattern = '\w+(\.?\w+)*'

    porter = PorterStemmer()

    def __init__(self):
        ## Open the file and get all words
        with open('keywords.txt') as f:
            word_list = f.readlines()

        ## lowercase and stem
        self.keywords = set([self.porter.stem(word.strip().lower()) for word in word_list])

    def get_keywords_present(self, link, anchor_text):
        link_words = [match.group() for match in re.finditer(self.pattern, link, re.M | re.I)]
        anchor_text_words = [match.group() for match in re.finditer(self.pattern, anchor_text, re.M | re.I)]
        if(len(anchor_text_words)!=0 ):
            link_words = link_words + anchor_text_words
        url_words = set(link_words)
        lowercase_stemmed_words = {self.porter.stem(word.strip().lower()) for word in url_words}
        common_words = lowercase_stemmed_words.intersection(self.keywords)
        return(common_words)

    def is_link_relavant(self, link, anchor_text):
        common_words = self.get_keywords_present(link, anchor_text)
        if(len(common_words) >= 1):
            return {"answer": True, "priority": len(common_words)}
        else:
            return {"answer": False, "priority": len(common_words)}