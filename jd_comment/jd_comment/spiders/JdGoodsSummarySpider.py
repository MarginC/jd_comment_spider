# -*- coding: utf-8 -*-
import scrapy
import json
import redis
from jd_comment.items import JdGoodsSummaryItem
from scrapy.utils.project import get_project_settings


class JdgoodssummarySpider(scrapy.Spider):
    name = "JdGoodsSummary"
    allowed_domains = ["club.jd.com"]
    custom_settings = {
            'ITEM_PIPELINES': {
            'jd_comment.pipelines.JdGoodsSummaryPipeline': 1,
         }
     }

    def start_requests(self):
        settings = get_project_settings()
        self.redis = redis.Redis(
            host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'))
        self.summary_task = settings.get('REDIS_SUMMARY_TASK_KEY',
            'jd_summary_task')
        for task in self.redis.smemembers(self.summary_task):
            _json = json.loads(task)
            yield scrapy.Request(_json['url'],
                meta={'referenceId': _json['referenceId']},
                callback=self.parseGoodsSummary)

    def parseGoodsSummary(self, response):
        summary = json.loads(response.text)
        try:
            del summary['comments']
            del summary['hotCommentTagStatistics']
            del summary['vTagStatistics']
        except:
            pass
        item = JdGoodsSummaryItem()
        try:
            item['maxPage'] = summary['maxPage']
        except:
            yield scrapy.Request(response.url,
                meta={'referenceId': response.meta['referenceId']},
                dont_filter=True, callback=self.parseGoodsSummary)
        item['referenceId'] = response.meta['referenceId']
        item['summary'] = summary
        yield item
