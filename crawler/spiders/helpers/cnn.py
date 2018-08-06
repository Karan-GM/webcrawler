from scrapy.linkextractors import LinkExtractor

class Cnn():
    link_extractor = LinkExtractor(
        allow_domains = ['cnn.com'],
        restrict_xpaths = [
            '//*[@class="l-container"]'
        ],
        canonicalize=True,
        unique=True
    )