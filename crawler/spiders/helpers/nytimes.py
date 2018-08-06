from scrapy.linkextractors import LinkExtractor

class NyTimes():
    link_extractor = LinkExtractor(
        allow_domains = ['nytimes.com'],
        restrict_xpaths = [
            '//*[@id="story"]',
            '//*[@id="related-combined-coverage"]',
            '//*[@class="RelatedCoverage-relatedcoverage--LmkKX"]'
        ],
        canonicalize=True,
        unique=True
    )