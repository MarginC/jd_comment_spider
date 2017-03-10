# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import re
import redis
from scrapy.utils.project import get_project_settings


class JdGoodsListPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        self.redis = redis.Redis(
            host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'))
        try:
            self.goods_list = settings.get('REDIS_GOODS_LIST_KEY')
        except:
            self.goods_list = 'jd_goods_list'
        pass

    def process_item(self, item, spider):
        match = re.match(r'^http://item.jd.com/(\d+)\.html', item['url'])
        item['referenceId'] = match.group(1)
        self.redis.sadd(self.goods_list,
            json.dumps(dict(item), ensure_ascii=False))
        pass

    def close_spider(self, spider):
        self.redis.save()
        pass


class JdGoodsSummaryPipeline(object):
    def __init__(self):
        self.file = codecs.open('jd_goods_summary.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        pass

    def close_spider(self, spider):
        self.file.close()


class JdGoodsPricePipeline(object):
    def __init__(self):
        self.file = codecs.open('jd_goods_price.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        pass

    def close_spider(self, spider):
        self.file.close()


class JdCommentPipeline(object):
    def __init__(self):
        self.file = codecs.open('jd_comment.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        pass

    def close_spider(self, spider):
        self.file.close()

