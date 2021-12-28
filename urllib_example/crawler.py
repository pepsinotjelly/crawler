import os
import re
import urllib.error
import http.cookiejar
from urllib.request import Request, urlopen

import xlwt
from bs4 import BeautifulSoup

from urllib_example.items import BookItem


class Crawler:
    def start(self):
        pass

    def request(self):
        pass

    def download(self, book_list, SAVE_PATH="./resource/book_data.xls"):
        workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
        sheet = workbook.add_sheet("豆瓣读书top250", cell_overwrite_ok=True)
        sheet.write(0, 0, 'number')
        sheet.write(0, 1, 'name')
        sheet.write(0, 2, 'info')
        sheet.write(0, 3, 'star')
        sheet.write(0, 4, 'quote')
        sheet.write(0, 5, 'reader')
        for i in range(len(book_list)):
            print("saving No.%d" % (i + 1))
            book = book_list[i]
            sheet.write(i + 1, 0, i + 1)
            sheet.write(i + 1, 1, book.name)
            sheet.write(i + 1, 2, book.info)
            sheet.write(i + 1, 3, book.star)
            sheet.write(i + 1, 4, book.quote)
            sheet.write(i + 1, 5, book.reader)
        workbook.save(SAVE_PATH)

    def parse_item(self, RESOURCE_ROOT):
        booklist = []
        count = 0
        for data in os.listdir(RESOURCE_ROOT):
            print("parsing page:---------------------------------------", count)
            print("filename:---------------------------", data)
            count += 1
            with open(RESOURCE_ROOT + data, 'r', encoding='UTF-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                for i in range(len(soup.find_all('tr', class_='item'))):
                    book = BookItem()
                    book.name = \
                    soup.find_all('tr', class_='item')[i].find_all('div', class_='pl2')[0].find('a').text.strip().split(
                        ' ')[0].strip()
                    book.info = soup.find_all('tr', class_='item')[i].find_all('p', class_='pl')[0].text
                    book.star = soup.find_all('tr', class_='item')[i].find_all('span', class_='rating_nums')[0].text
                    if soup.find_all('tr', class_='item')[i].find_all('span', class_='inq'):
                        book.quote = soup.find_all('tr', class_='item')[i].find_all('span', class_='inq')[0].text
                    else:
                        book.quote = ""
                    book.reader = self.parse_number(
                        soup.find_all('tr', class_='item')[i].find_all('span', class_='pl')[0].text)
                    booklist.append(book)
        return booklist

    def parse_number(self,target):
        res = ''
        for i in range(len(target)):
            if '0' <= target[i] <= '9':
                res += target[i]
        return res.strip()


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/96.0.4664.110 Safari/537.36 '
HEADER = {
    'User-Agent': USER_AGENT,
    'Referer': 'https://book.douban.com/top250',
    'Cookie': 'bid=fLAdqpnsfRE; __utmc=30149280; __utmc=81379588; '
              '__utmz=30149280.1640321301.3.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; '
              '__utmz=81379588.1640321301.3.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; '
              'push_noty_num=0; push_doumail_num=0; dbcl2="247235182:DmC9SsZ2iE4"; ck=0Tux; __utmv=30149280.24723; '
              '_pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1640579448%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; '
              '_pk_ses.100001.3ac3=*; ap_v=0,6.0; __utma=30149280.1503170269.1640066250.1640321301.1640579448.4; '
              '__utma=81379588.95857263.1640066250.1640321301.1640579448.4; __utmb=30149280.2.10.1640579448; '
              '__utmb=81379588.2.10.1640579448; '
              '_pk_id.100001.3ac3=021988dc59405135.1640066250.4.1640579466.1640324096. '
}
RESOURCE_PATH = './book_request/resource/'


def url_maker(page=0):
    origin_url = "https://book.douban.com/top250"
    form_data = {
        'start': page
    }
    data = urllib.parse.urlencode(form_data)
    url = origin_url + '?' + data
    return url


def request_demo(page=0):
    url = url_maker(page)
    request = Request(url, headers=HEADER)
    return request


def download_picture(data, page):
    patten = r'https://img[0-9].doubanio.com/view/subject/s/public/s[0-9]{7}.jpg|https://img[0-9].doubanio.com/view/subject/s/public/s[0-9]{8}.jpg'
    pat = re.compile(patten)
    img_urls = re.findall(pat, str(data))
    print(img_urls)
    print(len(img_urls))
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
        print("Success!")


def use_proxy(is_write, page):
    # 创建代理
    proxy_handler = urllib.request.ProxyHandler({
        'http': '218.78.22.146:443',
        'http': '223.100.166.3',
        'http': '113.254.178.224',
        'http': '115.29.170.58',
        'http': '117.94.222.233'
    })
    # 创建opener
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)
    use_demo(is_write, page)


def use_demo(is_write, page):
    request = request_demo(page)
    try:
        response = urlopen(request)
        html = response.read()
        if is_write:
            f = open(RESOURCE_PATH + "book_response/bookList_" + str(page) + ".html", "wb")
            f.write(html)
            f.close
            download_picture(html, page)
        print(response.geturl())
        print(response.getcode())
        print(response.info())
        response.close()
    except urllib.error.HTTPError as e:
        print(e.reason)
        print(e.code)
        print(e.headers)


def do_request(is_write, if_proxy):
    for i in range(10):
        page = i * 25
        if if_proxy:
            use_proxy(is_write, page)
        else:
            use_demo(is_write, page)
