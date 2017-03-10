# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs

class ProxyPipeline(object):
    def __init__(self):
        self.file = codecs.open('proxy_list', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = 'http://{0}:{1}\n'.format(item['ipAddress'], item['port'])
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

