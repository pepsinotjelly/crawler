import os
import re
import urllib.error
import http.cookiejar
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import utils

import xlwt
from bs4 import BeautifulSoup
from config.config import HEADER, RESOURCE_PATH, USER_AGENT
from urllib_example.items import BookItem


class Crawler:
    wait_pool = set()
    used_pool = set()
    is_write = False  # 是否重写已保存的图片和页面

    def __init__(self, is_write):
        self.wait_pool.add('https://book.douban.com/top250')
        self.used_pool.clear()
        self.is_write = is_write
        print("==========================INIT DONE==========================")

    def start(self):
        print("========================REQUEST START========================")
        while len(self.wait_pool) > 0:
            self.send_request(is_write=self.is_write)

    def create_url(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        for i in range(len(soup.find_all('div', class_='paginator'))):
            url = soup.find_all('div', class_='paginator')[0].find_all('span', class_='next')[0].find('a').attrs['href']
            return url

    def batch_create_url(self, html):
        url_set = set()
        soup = BeautifulSoup(html, 'html.parser')
        for i in range(len(soup.find_all('div', class_='paginator')[0].find_all('a'))):
            url = soup.find_all('div', class_='paginator')[0].find_all('a')[i].attrs['href']
            url_set.add(url)
        return url_set

    def check_pool(self):
        if not self.wait_pool:
            return None
        url = self.wait_pool.pop()  # 待爬池url减少
        self.used_pool.add(url)  # 记录已经爬取的url
        return url

    def update_pool(self, html):
        url_set = self.batch_create_url(html)
        for url in self.used_pool.intersection(url_set):
            url_set.discard(url)
        self.wait_pool.update(url_set)

    def send_request(self, is_write):
        url = self.check_pool()
        if url is None:
            print("pool error,please check wait_pool!")
            return
        request = Request(url, headers=HEADER)
        self.create_proxy()
        page = utils.parse_number(urlparse(url).query)
        try:
            response = urlopen(request)
            html = response.read()
            if is_write==True:
                self.download_page(html=html, page=page)
                self.download_picture(data=html, page=page)
            self.update_pool(html)
            print(response.geturl())
            print(response.getcode())
            print(response.info())
            response.close()
        except urllib.error.HTTPError as e:
            response.close()
            print(e.reason)
            print(e.code)
            print(e.headers)

    def create_proxy(self):
        proxy_handler = urllib.request.ProxyHandler({
            'http': '218.78.22.146:443',
            'http': '223.100.166.3',
            'http': '113.254.178.224',
            'http': '115.29.170.58',
            'http': '117.94.222.233'
        })
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)

    def download_page(self, html, page):
        if page is None or page == '':
            return
        f = open(RESOURCE_PATH + "book_response/bookList_" + str(page) + ".html", "wb")
        f.write(html)
        f.close

    def download_picture(self, data, page):
        print("===================START DOWNLOAD PICTURE================")
        if page is None or page == '':
            return
        patten = r'https://img[0-9].doubanio.com/view/subject/s/public/s[0-9]{7}.jpg|https://img[0-9].doubanio.com/view/subject/s/public/s[0-9]{8}.jpg'
        pat = re.compile(patten)
        img_urls = re.findall(pat, str(data))
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', USER_AGENT)]
        urllib.request.install_opener(opener)
        for img in range(len(img_urls)):
            print("Downloading Picture No.%d with url:%s" % (img, img_urls[img]))
            try:
                urllib.request.urlretrieve(img_urls[img],
                                           RESOURCE_PATH + "book_img/img_" + str(page) + "_" + str(img) + ".jpg")
            except urllib.error.HTTPError as e:
                print(e.headers)
                urllib.request.urlretrieve(img_urls[img],
                                           RESOURCE_PATH + "book_img/img_" + str(page) + "_" + str(img) + ".jpg")
            print("===========================SUCCESS===========================")

    def download_item(self, SAVE_PATH="./book_request/resource/book_data.xls"):
        print("====================START DOWNLOAD DATA====================")
        book_list = self.parse_item()
        workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
        sheet = workbook.add_sheet("豆瓣读书top250", cell_overwrite_ok=True)
        sheet.write(0, 0, 'number')
        sheet.write(0, 1, 'name')
        sheet.write(0, 2, 'info')
        sheet.write(0, 3, 'star')
        sheet.write(0, 4, 'quote')
        sheet.write(0, 5, 'reader')
        sheet.write(0, 6, 'date')
        sheet.write(0, 7, 'price')
        for i in range(len(book_list)):
            print("=======================SAVING NO.%d=========================" % (i + 1))
            book = book_list[i]
            sheet.write(i + 1, 0, i + 1)
            sheet.write(i + 1, 1, book.name)
            sheet.write(i + 1, 2, book.info)
            sheet.write(i + 1, 3, book.star)
            sheet.write(i + 1, 4, book.quote)
            sheet.write(i + 1, 5, book.reader)
            sheet.write(i + 1, 6, book.date)
            sheet.write(i + 1, 7, book.price)
        workbook.save(SAVE_PATH)

    def parse_item(self, RESOURCE_ROOT='./book_request/resource/book_response/'):
        print("====================START PARSING ITEM====================")
        booklist = []
        for data in os.listdir(RESOURCE_ROOT):
            with open(RESOURCE_ROOT + data, 'r', encoding='UTF-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                for i in range(len(soup.find_all('tr', class_='item'))):
                    book = BookItem()
                    book.name = \
                        soup.find_all('tr', class_='item')[i].find_all('div', class_='pl2')[0].find(
                            'a').text.strip().split(
                            ' ')[0].strip()
                    book.info = soup.find_all('tr', class_='item')[i].find_all('p', class_='pl')[0].text
                    book.star = soup.find_all('tr', class_='item')[i].find_all('span', class_='rating_nums')[0].text
                    if soup.find_all('tr', class_='item')[i].find_all('span', class_='inq'):
                        book.quote = soup.find_all('tr', class_='item')[i].find_all('span', class_='inq')[0].text
                    else:
                        book.quote = ""
                    book.reader = utils.parse_number(
                        soup.find_all('tr', class_='item')[i].find_all('span', class_='pl')[0].text)
                    other_information = utils.parse_price_and_date(book.info)
                    book.price = other_information.get('price')
                    book.date = other_information.get('date')
                    booklist.append(book)
        return booklist
