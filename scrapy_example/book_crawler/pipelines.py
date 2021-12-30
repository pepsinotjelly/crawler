# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy_example.book_crawler import settings
import xlwt
import scrapy_example.util as util
from scrapy_example.book_crawler.items import BookItem

image_store = settings.IMAGES_STORE


class TutorialPipeline:
    def __init__(self):
        self.workbook = None
        self.sheet = None
        self.pos = 1

    def open_spider(self, spider):
        if util.is_write:
            self.workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 开启爬虫时调用
            self.sheet = self.workbook.add_sheet("豆瓣读书top250", cell_overwrite_ok=True)
            self.sheet.write(0, 0, 'number')
            self.sheet.write(0, 1, 'name')
            self.sheet.write(0, 2, 'info')
            self.sheet.write(0, 3, 'star')
            self.sheet.write(0, 4, 'reader')
            # self.sheet.write(0, 4, 'quote')

    def close_spider(self, spider):
        if util.is_write:
            self.workbook.save("./book_crawler/resource/book_data.xls")
        util.show(RESOURCE_ROOT="./book_crawler/resource/")

    def process_item(self, item, spider):
        if util.is_write:
            print("=======================SAVING NO.%d=========================" % (self.pos))
            self.sheet.write(self.pos, 0, self.pos)
            self.sheet.write(self.pos, 1, item['name'])
            self.sheet.write(self.pos, 2, item['info'])
            self.sheet.write(self.pos, 3, item['star'])
            # self.sheet.write(self.pos, 4, item['quote'])
            self.sheet.write(self.pos, 4, item['reader'])
            self.pos += 1
            return item
        else:
            pass
















    # def get_media_requests(self, item, info):
    #     if isinstance(item, BookItem):
    #         item['actors'] = item['actors'].replace(' ', '')
    #         item['actors'] = item['actors'].replace('\n', '')
    #         yield Request(item['image_url'])
    #
    # def file_name(self, request, respond, info):
    #     return request.url.split('/')[-1]
    #
    # def item_completed(self, results, item, info):
    #     paths = [result['path'] for status, result in results if status]
    #     if not paths:
    #         raise DropItem('Failed to download photo.')
    #     else:
    #         os.rename(image_store + '/' + paths[0], image_store + '/' + item['name'] + '.jpg')
    #     return item
