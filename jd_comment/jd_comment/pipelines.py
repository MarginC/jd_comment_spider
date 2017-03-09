# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import re
import redis


class JdGoodsListPipeline(object):
    def __init__(self):
        self.file = codecs.open('jd_goods_list.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        match = re.match(r'^http://item.jd.com/(\d+)\.html', item['url'])
        item['referenceId'] = match.group(1)
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class JdGoodsSummaryPipeline(object):
    def __init__(self):
        self.file = codecs.open('jd_comment_summarry.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class JdCommentPipeline(object):
    def __init__(self):
        self.file = codecs.open('jd_comment.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        self.file.close()

