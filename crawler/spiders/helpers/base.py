from scrapy.linkextractors import LinkExtractor

class Base():
    link_extractor = LinkExtractor(
        canonicalize=True,
        unique=True
    )