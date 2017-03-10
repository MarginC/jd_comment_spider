# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ipAddress = scrapy.Field()
    port = scrapy.Field()
    code = scrapy.Field()
    country = scrapy.Field()
    anonymity = scrapy.Field()
    google = scrapy.Field()
    https = scrapy.Field()
    lastChecked = scrapy.Field()
    pass
