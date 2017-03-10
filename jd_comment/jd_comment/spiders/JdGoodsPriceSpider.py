# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from jd_comment.items import JdGoodsPriceItem

class JdgoodspriceSpider(scrapy.Spider):
    name = "JdGoodsPrice"
    allowed_domains = ["p.3.cn"]
    custom_settings = {
            'ITEM_PIPELINES': {
            'jd_comment.pipelines.JdGoodsPricePipeline': 1,
         }
     }

    def __generateUrl(self, referenceId):
        return 'http://p.3.cn/prices/mgets?skuIds=J_{0}'.format(referenceId)

    def start_requests(self):
        with open('jd_goods_list.json') as f:
            for line in f.readlines():
                goods = json.loads(line)
                url = self.__generateUrl(goods['referenceId'])
                yield scrapy.Request(url, meta={'referenceId': goods['referenceId']}, 
                    callback=self.parseGoodsPrice)

    def parseGoodsPrice(self, response):
        try:
            price = json.loads(response.text)[0]
        except Exception as e:
            yield scrapy.Request(response.url, meta={'referenceId': response.meta['referenceId']}, callback=self.parseGoodsPrice)
        item = JdGoodsPriceItem()
        item['referenceId'] = response.meta['referenceId']
        item['price'] = price['p']
        item['m'] = price['m']
        item['op'] = price['op']
        yield item
