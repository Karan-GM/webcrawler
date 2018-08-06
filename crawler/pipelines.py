# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import XmlItemExporter

class CrawlerPipeline(object):

    def process_item(self, item, spider):
        filename = item['filename']
        file = open('data/{}.xml'.format(filename[0]), 'wb')
        exporter = XmlItemExporter(file)
        exporter.start_exporting()
        exporter.fields_to_export = ["docno", "http_header", "title", "text", "html_source", "author", "depth", "url"]
        exporter.export_item(item)
        exporter.finish_exporting()
        file.close()
        return item
