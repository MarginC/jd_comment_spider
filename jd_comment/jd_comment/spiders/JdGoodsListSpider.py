# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from jd_comment.items import JdGoodsListItem

class JdgoodslistSpider(scrapy.Spider):
    name = "JdGoodsList"
    allowed_domains = ["list.jd.com"]
    custom_settings = {
            'ITEM_PIPELINES': {
            'jd_comment.pipelines.JdGoodsListPipeline': 1,
         }
     }
    cat_list_file = 'cat_list'
    start_page = 1
    end_page = 10

    def __generateUrl(self, cat, page):
        return 'http://list.jd.com/list.html?cat={0}&ev=exbrand_7817&page={1}&delivery=1&stock=0&sort=sort_totalsales15_desc&trans=1&JL=4_7_0#J_main'.format(cat, page)

    def start_requests(self):
        try:
            f = open(self.cat_list_file)
            for cat in f.readlines():
                url = self.__generateUrl(cat, 1)
                yield scrapy.Request(url, meta={'cat': cat}, callback=self.parseGoodsPages)
        except Exception as e:
            print(e)

    def parseGoodsPages(self, response):
        pages = response.xpath('//span[@class="fp-text"]/i/text()').extract()
        cat = response.meta['cat']
        for page in range(int(pages[0])):
            url = self.__generateUrl(cat, page)
            yield scrapy.Request(url, callback=self.parseGoodsList)

    def parseGoodsList(self, response):
        lis = response.xpath('//div[@class="ml-wrap"]/div[@id="plist"]/ul/li[@class="gl-item"]/div')
        for sel in lis:
            item = JdGoodsListItem()
            try:
                item['name'] = sel.xpath('div[@class="p-name"]/a/em/text()').extract()[0]
                item['url'] = 'http:' + sel.xpath('div[@class="p-name"]/a/@href').extract()[0]
            except Exception as e:
                yield scrapy.Request(response.url, callback=self.parseGoodsList)
            yield item

