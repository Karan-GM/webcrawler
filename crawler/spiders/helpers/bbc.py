from scrapy.linkextractors import LinkExtractor

class Bbc():
    link_extractor = LinkExtractor(
        allow_domains = ['bbc.com'],
        restrict_xpaths = [
            '//*[@class="story-body"]',
            '//*[@class="story-more"]'
        ],
        canonicalize=True,
        unique=True
    )