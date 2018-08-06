# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.loader import ItemLoader
from scrapy.http import Request
from crawler.items import CrawlerItem
import lxml.etree
import lxml.html
from scrapy import signals
from scrapy.exceptions import CloseSpider
from crawler.spiders.factory import Factory
from scrapy.http import HtmlResponse

class CustomSpider(CrawlSpider):
    name = 'custom'
    factory = Factory()
    start_urls = factory.start_urls
    rules = factory.rules
    total_documents = 20000

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CustomSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    ## Overriding start_requests to make start_url's as part of duplicate filter
    def start_requests(self):
        ## Set Seed URl priority
        self.start_time = self.factory.summary.set_start_time()
        seed_url_priority = len(self.factory.keywords.keywords)+1
        for url in self.start_urls:
            request = Request(url, priority=seed_url_priority)
            request.meta['parent_url'] = None
            request.meta['depth'] = 0
            request.meta['link_text'] = None
            # print('Priority : {} with Request: {}'.format(request.priority, request.url))
            yield request

    ## Function to obtain start_url_response
    def parse_start_url(self, response):
        return(self.parse_page(response))

    ## Function to filter links, check for robots.txt and reorder them
    def link_filtering(self, links):
        return links

    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                r.meta['parent_url'] = response.url
                r.meta['depth'] = response.meta['depth'] + 1
                yield rule.process_request(r)

    def request_filtering(self, request):
        is_relavant = self.factory.keywords.is_link_relavant(request.url, request.meta['link_text'])
        if(is_relavant['answer'] == True):
            request.priority = is_relavant['priority']
            # print("New Request {}".format(request.url))
            # print("Parent Request {}".format(request.meta))
            # print('Priority : {} with Request: {}'.format(request.priority, request.url))
            return request
        else:
            # self.logger.info('Dropping Request %s', request.url)
            return None

    def parse_page(self, response):
        item = ItemLoader(item=CrawlerItem(), response=response)
        if self.factory.summary.get_count() > self.total_documents:
            self.logger.info('Exiting, as we have got sufficient documents')
            raise CloseSpider('Exiting, as we have got sufficient documents')

        url = response.request.url
        headers = response.headers
        title = response.xpath('//title/text()').extract()[0]
        root = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")
        text = lxml.html.tostring(root, method="text", encoding='unicode')

        html_source = response.text
        depth = response.meta['depth']
        updated_count = self.factory.summary.update_count()

        ## Updating the outlink dictionary
        seen = set()
        for n, rule in enumerate(self._rules):
            outlinks_url = [lnk.url for lnk in rule.link_extractor.extract_links(response) if lnk not in seen]
        self.factory.summary.update_outlinks_dict(response.url, outlinks_url)
        ## Updating the inlink dictionary
        self.factory.summary.update_inlinks_dict(response.url, response.meta['parent_url'])

        item.add_value('docno', url)
        item.add_value('http_header', str(headers))
        item.add_value('title', title)
        item.add_value('text', text)
        item.add_value('html_source', html_source)
        item.add_value('author', "Karan Gulur Muralidhar")
        item.add_value('depth', depth)
        item.add_value('url', url)
        item.add_value('filename', updated_count)

        # print(">>>>>>>>>> RESULT")
        # print('Count: {} and URL: {}'.format(self.factory.summary.get_count(), response.url))
        # print('Priority: {} and Depth: {}'.format(response.request.priority, self.depth_dict[response.url]))
        # print(">>>>>>>>>>")
        self.logger.info('Count: %s', self.factory.summary.get_count())
        self.logger.info("Depth: %s", response.meta['depth'])
        self.logger.info("Response URL: " + response.url)
        self.logger.info("Parent: %s", response.meta['parent_url'])
        self.logger.info("Link Text: %s", response.meta['link_text'])
        self.logger.info("")

        return(item.load_item())

    def spider_closed(self, spider):
        self.logger.info('@@@@@@@@@@ Closing {} spider'.format(spider.name))
        self.end_time = self.factory.summary.set_end_time()
        self.factory.summary.dump()
