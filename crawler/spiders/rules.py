from scrapy.spiders import Rule
from crawler.spiders.helpers.nbcnews import NbcNews
from crawler.spiders.helpers.wikipedia import Wikipedia
from crawler.spiders.helpers.nytimes import NyTimes
from crawler.spiders.helpers.bbc import Bbc
from crawler.spiders.helpers.cnn import Cnn
from crawler.spiders.helpers.base import Base

class Rules():
    nbcnews_link_extractor = NbcNews().link_extractor
    nytimes_link_extractor = NyTimes().link_extractor
    bbc_link_extractor = Bbc().link_extractor
    cnn_link_extractor = Cnn().link_extractor
    wikipedia_link_extractor = Wikipedia().link_extractor
    base_link_extractor = Base().link_extractor
    rules = (
            Rule(nbcnews_link_extractor, callback='parse_page', process_links='link_filtering', process_request='request_filtering', follow=True),
            Rule(nytimes_link_extractor, callback='parse_page', process_links='link_filtering', process_request='request_filtering', follow=True),
            Rule(bbc_link_extractor, callback='parse_page', process_links='link_filtering', process_request='request_filtering', follow=True),
            Rule(cnn_link_extractor, callback='parse_page', process_links='link_filtering', process_request='request_filtering', follow=True),
            Rule(wikipedia_link_extractor, callback='parse_page', process_links='link_filtering',process_request='request_filtering', follow=True),
            Rule(base_link_extractor, callback='parse_page', process_links='link_filtering', process_request='request_filtering', follow=True),
    )