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
        while True:
            task = self.redis.spop(self.comment_task)
            if not task:
                break
            _json = json.loads(task)
            yield scrapy.Request(_json['url'],
                meta={'maxPage': _json['maxPage'], 'page': _json['page']},
                callback=self.parseComment)

    def parseComment(self, response):
        page = response.meta['page']
        maxPage = response.meta['maxPage']
        try:
            summary = json.loads(response.text)
            comments = summary['comments']
            if comments is None and int(page) < int(maxPage):
                self.redis.sadd(self.comment_task, json.dumps(
                    {'maxPage': maxPage, 'page': page, 'url': response.url}, 
                    ensure_ascii=False))
                return 
        except:
            self.redis.sadd(self.comment_task, json.dumps(
                {'maxPage': maxPage, 'page': page, 'url': response.url}, 
                ensure_ascii=False))
            return
        for comment in comments:
            item = JdCommentItem()
            item['commentId'] = comment['id']
            item['content'] = comment['content']
            item['creationTime'] = comment['creationTime']
            item['referenceId'] = comment['referenceId']
            item['referenceName'] = comment['referenceName']
            try:
                item['referenceTime'] = comment['referenceTime']
            except:
                pass
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
