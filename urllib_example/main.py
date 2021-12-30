import os

import urllib_example.crawler as ec
from bs4 import BeautifulSoup
import utils


def print_hi(name):
    print(f'Hi, {name}')

    if __name__ == '__main__':
        book_crawler = ec.Crawler(is_write=False, is_online_data=False)
        book_crawler.start()  # 爬取并保存页面信息
        book_crawler.download_item()  # 解析并存储数据
        utils.show()  # 展示图表


if __name__ == '__main__':
    print_hi('Request!')
