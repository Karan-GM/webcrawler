# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    docno = scrapy.Field()
    http_header = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    html_source = scrapy.Field()
    author = scrapy.Field()
    depth = scrapy.Field()
    url = scrapy.Field()
    filename = scrapy.Field()

    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({"docno": self["docno"]})