from scrapy.linkextractors import LinkExtractor

class NbcNews():
    link_extractor = LinkExtractor(
        # allow = ['.*www.nbcnews.com\/storyline.*'],
        allow=['.*www.nbcnews.com.*'],
        allow_domains = ['nbcnews.com'],
        restrict_xpaths = [
            '//*[@id="top-stories"]',
            '//*[@class="gridContainer___3alrm gridContainer___2Sgv0"]'
        ],
        canonicalize=True,
        unique=True
    )