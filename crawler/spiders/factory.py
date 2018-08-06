from crawler.spiders.seed_url import SeedUrl
from crawler.spiders.rules import Rules
from crawler.spiders.keywords_helper import Keywords
from crawler.spiders.summary import Summary

class Factory():
    start_urls = SeedUrl().start_urls

    rules = Rules().rules

    keywords = Keywords()

    summary = Summary()