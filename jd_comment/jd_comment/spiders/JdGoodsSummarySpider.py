# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from jd_comment.items import JdGoodsSummary

class JdgoodssummarySpider(scrapy.Spider):
    name = "JdGoodsSummary"
    allowed_domains = ["club.jd.com"]
    custom_settings = {
            'ITEM_PIPELINES': {
            'jd_comment.pipelines.JdGoodsSummaryPipeline': 1,
         }
     }

    def __generateUrl(self, referenceId):
        return 'http://club.jd.com/comment/productPageComments.action?productId={0}&score=0&sortType=5&page=0&pageSize=10'.format(referenceId)

    def start_requests(self):
        with open('jd_goods_list.json') as f:
            for line in f.readlines():
                print(line)
                goods = json.loads(line)
                url = self.__generateUrl(goods['referenceId'])
                print(url)
                yield scrapy.Request(url, meta={'referenceId': goods['referenceId']}, 
                    callback=self.parseGoodsSummary)

    def parseGoodsSummary(self, response):
        try:
            summary = json.loads(response.text)
        except Exception as e:
            yield scrapy.Request(url, meta={'referenceId': response.meta['referenceId']},
                callback=self.parseGoodsSummary)
        try:
            del summary['comments']
            del summary['hotCommentTagStatistics']
            del summary['vTagStatistics']
        except Exception as e:
            pass
        item = JdGoodsSummary()
        item['referenceId'] = response.meta['referenceId']
        item['maxPages'] = summary['maxPage']
        item['summary'] = summary
        yield item
