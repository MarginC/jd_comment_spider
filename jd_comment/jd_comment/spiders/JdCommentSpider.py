# -*- coding: utf-8 -*-
import scrapy
import json
import redis
from jd_comment.items import JdCommentItem
from scrapy.utils.project import get_project_settings


class JdcommentSpider(scrapy.Spider):
    name = "JdComment"
    allowed_domains = ["club.jd.com"]
    custom_settings = {
            'ITEM_PIPELINES': {
            'jd_comment.pipelines.JdCommentPipeline': 1,
        }
    }
    set_name = 'comment_urls'

    def start_requests(self):
        settings = get_project_settings()
        self.redis = redis.Redis(
            host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'))
        self.comment_task = settings.get('REDIS_COMMENT_TASK_KEY',
            'jd_comment_task')
        for task in self.redis.smembers(self.comment_task):
            _json = json.loads(task)
            yield scrapy.Request(_json['url'],
                meta={'maxPage': _json['maxPage'], 'page': _json['page']},
                callback=self.parseComment)

    def parseComment(self, response):
        comments = []
        try:
            summary = json.loads(response.text)
            comments = summary['comments']
        except:
            response.request.dont_filter = True
            yield response.request
        page = response.meta['page']
        maxPage = response.meta['maxPage']
        if len(comments) == 0 and int(page) < int(maxPage):
            response.request.dont_filter = True
            yield response.request
        for comment in comments:
            item = JdCommentItem()
            item['commentId'] = comment['id']
            item['content'] = comment['content']
            item['creationTime'] = comment['creationTime']
            item['referenceId'] = comment['referenceId']
            item['referenceName'] = comment['referenceName']
            item['referenceTime'] = comment['referenceTime']
            item['score'] = comment['score']
            item['userLevelId'] = comment['userLevelId']
            item['userProvince'] = comment['userProvince']
            item['nickname'] = comment['nickname']
            item['userClient'] = comment['userClient']
            item['userLevelName'] = comment['userLevelName']
            item['plusAvailable'] = comment['plusAvailable']
            item['recommend'] = comment['recommend']
            item['userClientShow'] = comment['userClientShow']
            item['isMobile'] = comment['isMobile']
            item['days'] = comment['days']
            item['afterDays'] = comment['afterDays']
            try:
                item['hAfterUserComment'] = comment['hAfterUserComment']
            except:
                pass
            yield item
