# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from jd_comment.items import JdGoodsList

class JdgoodslistspiderSpider(scrapy.Spider):
    name = "JdGoodsListSpider"
    allowed_domains = ["list.jd.com"]
    start_urls = [
'http://list.jd.com/list.html?cat=737,794,798&ev=exbrand_7817&page=1&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main',
'http://list.jd.com/list.html?cat=737,794,870&ev=exbrand_7817&page=1&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main',
'http://list.jd.com/list.html?cat=737,794,13701&ev=exbrand_7817&page=1&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main',
'http://list.jd.com/list.html?cat=737,794,880&ev=exbrand_7817&page=1&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main',
'http://list.jd.com/list.html?cat=737,794,878&ev=exbrand_7817&page=1&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main',
'http://list.jd.com/list.html?cat=737,794,12392&ev=exbrand_7817&page=1&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main',
'http://list.jd.com/list.html?cat=737,794,12401&ev=exbrand_7817&page=1&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main',
'http://list.jd.com/list.html?cat=737,13297,13298&ev=exbrand_7817&page=1&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main',
'http://list.jd.com/list.html?cat=737,13297,1300&ev=exbrand_7817&page=1&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main',
'http://list.jd.com/list.html?cat=737,13297,13117&ev=exbrand_7817&page=1&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main',
'http://list.jd.com/list.html?cat=737,13297,13690&ev=exbrand_7817&page=1&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main',
'http://list.jd.com/list.html?cat=737,13297,13691&ev=exbrand_7817&page=1&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main',
]

    def parse(self, response):
        lis = response.xpath('//div[@class="ml-wrap"]/div[@id="plist"]/ul/li[@class="gl-item"]/div')
        for sel in lis:
            item = JdGoodsList()
            item['name'] = sel.xpath('div[@class="p-name"]/a/em/text()').extract()[0]
            item['url'] = 'http:' + sel.xpath('div[@class="p-name"]/a/@href').extract()[0]
#            buyIndex = sel.xpath('div[@class="p-commit"]/span/em/text()').extract()[0]
            yield item

