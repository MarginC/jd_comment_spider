# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdGoodsListItem(scrapy.Item):
    referenceId = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    pass


class JdGoodsSummaryItem(scrapy.Item):
    referenceId = scrapy.Field()
    maxPage = scrapy.Field()
    summary = scrapy.Field()
    pass


class JdGoodsPriceItem(scrapy.Item):
    referenceId = scrapy.Field()
    price = scrapy.Field()
    m = scrapy.Field()
    op = scrapy.Field()
    pass


class JdCommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    commentId = scrapy.Field()
    content = scrapy.Field()
    creationTime = scrapy.Field()
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
    recommend = scrapy.Field()
    userClientShow = scrapy.Field()
    isMobile = scrapy.Field()
    days = scrapy.Field()
    afterDays = scrapy.Field()
    hAfterUserComment = scrapy.Field()
    pass
