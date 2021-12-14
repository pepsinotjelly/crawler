# -*- coding: UTF-8 -*-
"""
@Project ：crawler 
@File    ：book_spider.py
@Author  ：Sonia.Suen
@Date    ：2021/12/13 12:55 PM
@Desc    ：
    start_requests(self)
    必须返回一个可迭代的请求（可以返回一个请求列表或编写一个生成器函数），蜘蛛将从中开始爬行。
    后续请求将从这些初始请求中依次生成。

    parse()是一个方法，将被调用来处理为每个请求下载的响应。
    response 参数是一个实例，TextResponse它保存页面内容并有更多有用的方法来处理它。
    该parse()方法通常解析响应，将抓取的数据提取为 dicts，并找到要遵循的新 URL 并Request从中创建新请求 ( )。
"""
from abc import ABC

import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from tutorial.book_crawler.items import BookItem


class TutorialSpider(CrawlSpider, ABC):
    name = 'books_item'  # 标识 Spider 。它在一个项目中必须是唯一的，即不能为不同的 Spider 设置相同的名称。
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/top250?start=0']
    rules = [Rule(LinkExtractor(allow=r'^https://book\.douban\.com/top250\?start=\d+$'),
                  callback='parse_item', follow=False)]

    def parse_item(self, response):
        print(response)
        # books_list = response.xpath('//div[@class="indent"]')
        # books_list = books_list.xpath('//div[@class="indent"]')
        book_list = response.xpath('//tr[@class="item"]')
        # for books_item in books_list:
            # books_item = books_item.xpath('//tr[@class="item"]')
        # print("-----------------------------------------")
        for book_item in book_list:
            book = BookItem()
            book['name'] = book_item.xpath('//div[@class="pl2"]/a/@title').get()
            book['info'] = book_item.xpath('//p[@class="pl"]/text()').get()  # 出版信息
            book['star'] = book_item.xpath('//span[@class="rating_nums"]/text()').get()  # 星级
            book['quote'] = book_item.xpath('//span[@class="inq"]/text()').get()
            book['image'] = book_item.xpath('//img/@src').get()
            yield book

