# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from jd_comment.items import JdCommentItem

class JdcommentSpider(scrapy.Spider):
    name = "JdComment"
    allowed_domains = ["club.jd.com"]
    custom_settings = {
            'ITEM_PIPELINES': {
            'jd_comment.pipelines.JdCommentPipeline': 1,
        }
    }
    set_name = 'comment_urls'

    def __generateUrl(self, referenceId, page):
        return 'http://club.jd.com/comment/productPageComments.action?productId={0}&score=0&sortType=5&page={1}&pageSize=10'.format(referenceId, page)

    def start_requests(self):
        with open('jd_goods_summary.json') as f:
            for line in f.readlines():
                goods = json.loads(line)
                referenceId = goods['referenceId']
                maxPage = goods['maxPage']
                for page in range(int(maxPage)):
                    url = self.__generateUrl(referenceId, page)
                    yield scrapy.Request(url, meta={'maxPage': maxPage, 'page': page}, callback=self.parseComment)

    def parseComment(self, response):
        comments = []
        try:
            summary = json.loads(response.text)
            comments = summary['comments']
        except Exception as e:
            response.request.dont_filter=True
            yield response.request
        page = response.meta['page']
        maxPage = response.meta['maxPage']
        if len(comments) == 0 and int(page) < int(maxPage):
            response.request.dont_filter=True
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
            except Exception as e:
                pass
            yield item
