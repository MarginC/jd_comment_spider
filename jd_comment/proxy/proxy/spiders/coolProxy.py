# -*- coding: utf-8 -*-
import scrapy
from proxy.items import ProxyItem


class CoolproxySpider(scrapy.Spider):
    name = "coolProxy"
    allowed_domains = ["www.cool-proxy.net"]
    start_urls = ['https://www.cool-proxy.net/proxies/'
        'http_proxy_list/sort:score/direction:desc/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'proxy.pipelines.ProxyPipeline': 1,
        }
    }

    def __genarateUrl(self, page):
        url = 'https://www.cool-proxy.net/proxies/' \
            'http_proxy_list/page:{0}/sort:score/direction:desc'.format(page)
        return url

    def parse(self, response):
        spans = response.xpath('//th[@class="pagination"]/span')
        try:
            pages = spans[-2].xpath('a/text()')[0].extract()
            for page in range(int(pages)):
                url = self.__genarateUrl(page + 1)
                yield scrapy.Request(url, callback=self.parseDetail)
        except Exception as e:
            print(e)

    def parseDetail(self, response):
        for tr in response.xpath('//tr'):
            item = ProxyItem()
            try:
                item['ipAddress'] = tr.xpath('td/text()')[0].extract()
                item['port'] = tr.xpath('td/text()')[1].extract()
            except Exception as e:
                print(e)
                continue
            try:
                item['country'] = tr.xpath('td/text()')[3].extract()
                item['anonymity'] = tr.xpath('td/text()')[5].extract()
                item['lastChecked'] = tr.xpath('td/text()')[9].extract()
            except:
                pass
            print(item)
            yield item
