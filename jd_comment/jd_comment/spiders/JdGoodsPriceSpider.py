# -*- coding: utf-8 -*-
import scrapy
import json
import redis
from jd_comment.items import JdGoodsPriceItem
from scrapy.utils.project import get_project_settings


class JdgoodspriceSpider(scrapy.Spider):
    name = "JdGoodsPrice"
    allowed_domains = ["p.3.cn"]
    custom_settings = {
            'ITEM_PIPELINES': {
            'jd_comment.pipelines.JdGoodsPricePipeline': 1,
         }
     }

    def start_requests(self):
        settings = get_project_settings()
        self.redis = redis.Redis(
            host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'))
        self.price_task = settings.get('REDIS_PRICE_TASK_KEY', 'jd_price_task')
        for task in self.redis.smemembers(self.price_task):
            _json = json.loads(task)
            yield scrapy.Request(_json['url'],
                meta={'referenceId': _json['referenceId']},
                callback=self.parseGoodsPrice)

    def parseGoodsPrice(self, response):
        try:
            price = json.loads(response.text)[0]
        except:
            yield scrapy.Request(response.url,
                meta={'referenceId': response.meta['referenceId']},
                dont_filter=True, callback=self.parseGoodsPrice)
        item = JdGoodsPriceItem()
        item['referenceId'] = response.meta['referenceId']
        item['price'] = price['p']
        item['m'] = price['m']
        item['op'] = price['op']
        yield item
