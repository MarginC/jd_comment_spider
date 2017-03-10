# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import redis
from scrapy.utils.project import get_project_settings
import proxy.proxyFilter as proxyFilter


class ProxyPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        self.redis = redis.Redis(
            host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'))
        try:
            self.proxy_list = settings.get('REDIS_PROXY_LIST_KEY')
            self.proxy_list_valid = settings.get('REDIS_PROXY_VALID_LIST_KEY')
        except:
            self.proxy_list = 'proxy_list'
            self.proxy_list_valid = 'proxy_valid_list'
        pass

    def process_item(self, item, spider):
        self.redis.sadd(self.proxy_list,
            json.dumps(dict(item), ensure_ascii=False))
        valid, elapsed = proxyFilter.proxy_test('{0}:{1}'.
            format(item.get('ipAddress'), item.get('port')))
        if valid:
            self.redis.zadd(self.proxy_list_valid,
                json.dumps(dict(item), ensure_ascii=False), elapsed)
        pass

    def close_spider(self, spider):
        self.redis.save()
        pass
