from scrapy.linkextractors import LinkExtractor

class Wikipedia():
    link_extractor = LinkExtractor(
        allow_domains = ['en.wikipedia.org'],
        restrict_xpaths = [
            '//*[@class="reflist columns references-column-width"]'
        ],
        canonicalize=True,
        unique=True
    )