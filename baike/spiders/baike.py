# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.url import urljoin_rfc
from scrapy.http import Request


class BaikeSpider(scrapy.Spider):
    name = 'baike'
    allowed_domains = ['baike.baidu.com']
    start_urls = [
    # 'https://baike.baidu.com/item/货币/85299'
    # 'https://baike.baidu.com/item/经济', 
    # 'https://baike.baidu.com/item/金融/860', 
    # 'https://baike.baidu.com/item/法律/84813', 
    # 'https://baike.baidu.com/item/战争/14004', 
    # 'https://baike.baidu.com/item/历史/360', 
    # 'https://baike.baidu.com/item/网络/143243'
    # 'https://baike.baidu.com/item/互联网/199186',
    # 'https://baike.baidu.com/item/人物/360', 
    # 'https://baike.baidu.com/item/自然/143243'
    # 'https://baike.baidu.com/item/地理/199186',
    # 'https://baike.baidu.com/item/娱乐/360'
    # 'https://baike.baidu.com/item/科学/143243',
    # 'https://baike.baidu.com/item/%E7%94%9F%E6%B4%BB/18684',
    'https://baike.baidu.com/item/文化/23624'
    # 'https://baike.baidu.com/item/%E6%95%B0%E5%AD%A6/107037?fr=aladdin'
    # 'https://baike.baidu.com/item/%E7%89%A9%E7%90%86%E5%AD%A6/313183'
    # 'https://baike.baidu.com/item/%E5%8C%96%E5%AD%A6'
    # 'https://baike.baidu.com/item/%E5%BB%BA%E7%AD%91%E5%AD%A6'
    # 'https://baike.baidu.com/item/%E5%BF%83%E7%90%86%E5%AD%A6/6215'
    # 'https://baike.baidu.com/item/%E7%A4%BE%E4%BC%9A%E5%AD%A6/283098'
    ]
    url_set = set()

    def parse(self, response):
        filename = response.url.split("/")[4]
        filename = urllib.parse.unquote(filename)
        summary = ''
        detail = ''
        urls = []
        with open('../corpus/part4/'+filename+'.txt', 'w', encoding='utf-8') as f:
            for lem in response.xpath("//div[@class='lemma-summary']"):
                for sel in lem.xpath(".//div[@class='para']"):
                    desc = sel.xpath('text()|a/text()').extract()
                    for des in desc:
                        summary += des
            # print(summary)
            
            for sel in response.xpath("//div[@class='para']"):
                titles = sel.xpath('a/text()').extract()
                links = sel.xpath('a/@href').extract()
                desc = sel.xpath('text()|a/text()').extract()
                for des in desc:
                    detail += des
                for title,link in zip(titles,links):
                    if link.find('/pic/') != -1:
                        continue
                    urls.append([title,link])
            # print(detail)
            # print(urls)
            f.write(detail)

        for name,url in urls:
            url = "https://baike.baidu.com"+url
            if url in BaikeSpider.url_set:
                pass
            else:
                print(url)
                BaikeSpider.url_set.add(url)
                yield Request(url, callback=self.parse)
