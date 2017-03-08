# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs


class JdGoodsListPipeline(object):
    def __init__(self):
        self.file = codecs.open('jd_goods_list', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        self.file.close()


class JdGoodsSummaryPipeline(object):
    def __init__(self):
        self.file = codecs.open('jd_goods_summarry', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        self.file.close()


class JdCommentPipeline(object):
    def __init__(self):
        self.file = codecs.open('jd_comment', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        self.file.close()

