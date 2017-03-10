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
        self.goods_list = settings.get('REDIS_GOODS_LIST_KEY', 'jd_goods_list')
        self.price_task = settings.get('REDIS_PRICE_TASK_KEY', 'jd_price_task')
        self.summary_task = settings.get('REDIS_SUMMARY_TASK_KEY', 'jd_summary_task')
        pass

    def __pushPriceTask(self, referenceId):
        url = 'http://p.3.cn/prices/mgets?skuIds=J_{0}'.format(referenceId)
        task = {'url': url, 'referenceId': referenceId}
        self.redis.sadd(self.price_task, json.dumps(task, ensure_ascii=False))
        pass

    def __pushSummaryTask(self, referenceId):
        url = 'http://club.jd.com/comment/productPageComments.action?' \
            'productId={0}&score=0&sortType=5&page=0&' \
            'pageSize=10'.format(referenceId)
        task = {'url': url, 'referenceId': referenceId}
        self.redis.sadd(self.summary_task, json.dumps(task, ensure_ascii=False))
        pass

    def process_item(self, item, spider):
        match = re.match(r'^http://item.jd.com/(\d+)\.html', item['url'])
        item['referenceId'] = match.group(1)
        self.__pushPriceTask(item['referenceId'])
        self.__pushSummaryTask(item['referenceId'])
        self.redis.sadd(self.goods_list,
            json.dumps(dict(item), ensure_ascii=False))
        pass

    def close_spider(self, spider):
        self.redis.save()
        pass


class JdGoodsSummaryPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        self.redis = redis.Redis(
            host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'))
        self.summary_list = settings.get('REDIS_SUMMARY_LIST_KEY',
            'jd_summary_list')
        self.comment_task = settings.get('REDIS_COMMENT_TASK_KEY',
            'jd_comment_task')
        pass

    def __generateCommentUrl(self, referenceId, page):
        return 'http://club.jd.com/comment/productPageComments.action?' \
            'productId={0}&score=0&sortType=5&page={1}&' \
            'pageSize=10'.format(referenceId, page)

    def __pushCommentTask(self, referenceId, maxPage):
        for page in range(int(maxPage)):
            url = self.__generateCommentUrl(referenceId, page)
            task = {'maxPage': maxPage, 'page': page, 'url': url}
            self.redis.sadd(self.comment_task,
                json.dumps(task, ensure_ascii=False))
        pass

    def process_item(self, item, spider):
        self.__pushCommentTask(item['referenceId'], item['maxPage'])
        self.redis.sadd(self.summary_list,
            json.dumps(dict(item), ensure_ascii=False))
        pass

    def close_spider(self, spider):
        self.redis.save()
        pass


class JdGoodsPricePipeline(object):
    def __init__(self):
        settings = get_project_settings()
        self.redis = redis.Redis(
            host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'))
        self.price_list = settings.get('REDIS_PRICE_LIST_KEY', 'jd_price_list')
        pass

    def process_item(self, item, spider):
        self.redis.sadd(self.price_list,
            json.dumps(dict(item), ensure_ascii=False))
        pass

    def close_spider(self, spider):
        self.redis.save()
        pass


class JdCommentPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        self.redis = redis.Redis(
            host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'))
        self.comment_list = settings.get('REDIS_COMMENT_LIST_KEY',
            'jd_comment_list')
        pass

    def process_item(self, item, spider):
        self.redis.sadd(self.comment_list,
            json.dumps(dict(item), ensure_ascii=False))
        pass

    def close_spider(self, spider):
        self.redis.save()
        pass

