# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    info = scrapy.Field()  # 出版信息
    star = scrapy.Field()  # 星级
    # quote = scrapy.Field()
    # image = scrapy.Field()
    reader = scrapy.Field()
    pass
