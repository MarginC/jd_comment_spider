# -*- coding: utf-8 -*-
import scrapy
from proxy.items import ProxyItem

class UsproxySpider(scrapy.Spider):
    name = "usproxy"
    allowed_domains = ["https://www.us-proxy.org/"]
    start_urls = ['https://www.us-proxy.org//']
    custom_settings = {
        'ITEM_PIPELINES': {
            'proxy.pipelines.ProxyPipeline': 1,
        }
    }

    def parse(self, response):
        for tr in response.xpath('//tr'):
            item = ProxyItem()
            try:
                item['ipAddress'] = tr.xpath('td/text()')[0].extract()
                item['port'] = tr.xpath('td/text()')[1].extract()
            except Exception as e:
                continue
            try:
                item['code'] = tr.xpath('td/text()')[2].extract()
                item['country'] = tr.xpath('td/text()')[3].extract()
                item['anonymity'] = tr.xpath('td/text()')[4].extract()
                item['google'] = tr.xpath('td/text()')[5].extract()
                item['https'] = tr.xpath('td/text()')[6].extract()
                item['lastChecked'] = tr.xpath('td/text()')[7].extract()
            except Exception as e:
                pass
            yield item
