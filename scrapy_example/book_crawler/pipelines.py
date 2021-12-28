# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy_example.book_crawler import settings

from scrapy_example.book_crawler.items import BookItem

image_store = settings.IMAGES_STORE


class TutorialPipeline:
    def process_item(self, item, spider):
        return item

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
