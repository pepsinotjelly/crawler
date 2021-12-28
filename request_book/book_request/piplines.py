from bs4 import BeautifulSoup
import os
import xlwt

from request_book.book_request.data_collection import RESOURCE_PATH
from request_book.book_request.items import BookItem


def data_filter(RESOURCE_ROOT="./resource/book_response/"):
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
                book.name = soup.find_all('tr', class_='item')[i].find_all('div', class_='pl2')[0].find('a').text.strip().split(
                        ' ')[0].strip()
                book.info = soup.find_all('tr', class_='item')[i].find_all('p', class_='pl')[0].text
                book.star = soup.find_all('tr', class_='item')[i].find_all('span', class_='rating_nums')[0].text
                if soup.find_all('tr', class_='item')[i].find_all('span', class_='inq'):
                    book.quote = soup.find_all('tr', class_='item')[i].find_all('span', class_='inq')[0].text
                else:
                    book.quote = ""
                book.reader = filter_number(soup.find_all('tr', class_='item')[i].find_all('span', class_='pl')[0].text)
                booklist.append(book)
    return booklist


def filter_number(target):
    res = ''
    for i in range(len(target)):
        if '0' <= target[i] <= '9':
            res += target[i]
    return res.strip()


def save_data(book_list, SAVE_PATH="./resource/book_data.xls"):
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


save_data(data_filter())
# data_filter()
