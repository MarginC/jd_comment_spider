# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdGoodsList(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    referenceId = scrapy.Field()
    pass


class JdGoodsSummary(scrapy.Item):
    referenceId = scrapy.Field()
    maxPages = scrapy.Field()
    pass


class JdCommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    commentId = scrapy.Field()
    content = scrapy.Field()
    createTime = scrapy.Field()
    referenceId = scrapy.Field()
    referenceName = scrapy.Field()
    referenceTime = scrapy.Field()
    score = scrapy.Field()
    userLevelId = scrapy.Field()
    userProvince = scrapy.Field()
    nickname = scrapy.Field()
    userClient = scrapy.Field()
    userLevelName = scrapy.Field()
    plusAvailable = scrapy.Field()
    recommand = scrapy.Field()
    userClientShow = scrapy.Field()
    isMobile = scrapy.Field()
    days = scrapy.Field()
    afterDays = scrapy.Field()
    pass
