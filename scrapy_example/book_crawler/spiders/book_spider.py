# -*- coding: UTF-8 -*-
"""
@Project ：crawler 
@File    ：book_spider.py
@Author  ：Sonia.Suen
@Date    ：2021/12/13 12:55 PM
@Desc    ：
"""
import copy
from abc import ABC

import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy_example.book_crawler.items import BookItem
import scrapy_example.util as util


def image_filter(image_list):
    image_list_v2 = copy.deepcopy(image_list)
    for i in range(len(image_list)):
        if image_list[i] == '/pics/read.gif':
            image_list_v2.remove(image_list[i])
    return image_list_v2


class TutorialSpider(CrawlSpider, ABC):
    name = 'books_item'  # 标识 Spider 。它在一个项目中必须是唯一的，即不能为不同的 Spider 设置相同的名称。
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/top250']
    rules = [Rule(LinkExtractor(allow=r'^https://book\.douban\.com/top250\?start=\d+$'),
                  callback='parse_item', follow=False)]

    def parse_item(self, response):
        item_list = response.xpath('//div[@class="indent"]')
        book_item = item_list.xpath('//tr[@class="item"]')

        name_list = book_item.xpath('//div[@class="pl2"]/a/@title').extract()
        info_list = book_item.xpath('//p[@class="pl"]/text()').extract()  # 出版信息
        star_list = book_item.xpath('//span[@class="rating_nums"]/text()').extract()  # 星级
        reader_list = book_item.xpath('//span[@class="pl"]').extract()

        # quote_list = book_item.xpath('//span[@class="inq"]/text()').extract()
        # image_list = image_filter(book_item.xpath('//img/@src').extract())

        for i in range(len(book_item)):
            book = BookItem()
            book['name'] = name_list[i]
            book['info'] = info_list[i]
            book['star'] = star_list[i]
            book['reader'] = util.parse_number(reader_list[i])
            # book['quote'] = quote_list[i]
            # book['image'] = image_list[i]
            yield book
