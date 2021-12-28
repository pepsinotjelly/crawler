from bs4 import BeautifulSoup
import os
import xlwt

from request_book.book_request.data_collection import RESOURCE_PATH
from request_book.book_request.items import BookItem


def data_filter(RESOURCE_ROOT="./resource/book_response/"):
    print(os.getcwd())
    booklist = []
    count=0
    for data in os.listdir(RESOURCE_ROOT):
        print("page:%d---------------------------------------",count)
        print(data)
        count += 1
        with open(RESOURCE_ROOT + data, 'r', encoding='UTF-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            tag = 0
            for i in range(len(soup.find_all('tr', class_='item'))):
                book = BookItem()
                book.name = soup.find_all('div', class_='pl2')[i].find('a').text.strip().split(' ')[0].strip()
                book.info = soup.find_all('p', class_='pl')[i].text
                book.star = soup.find_all('span', class_='rating_nums')[i].text
                book.quote = soup.find_all('span', class_='inq')[tag].text
                booklist.append(book)
    return booklist


def save_data(book_list, SAVE_PATH="./resource/book_data.xls"):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = workbook.add_sheet("豆瓣读书top250", cell_overwrite_ok=True)
    for i in range(len(book_list)):
        print("saving No.%d" % (i + 1))
        book = book_list[i]
        sheet.write(i, 0, i+1)
        sheet.write(i, 1, book.name)
        sheet.write(i, 2, book.info)
        sheet.write(i, 3, book.star)
        sheet.write(i, 4, book.quote)
    workbook.save(SAVE_PATH)  # 保存数据表


save_data(data_filter())
