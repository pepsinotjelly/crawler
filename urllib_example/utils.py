import re

import matplotlib.pyplot as plt
import pandas
import numpy as np
import scipy.stats as ss
import seaborn as sns

import xlrd


def show(RESOURCE_ROOT="./book_request/resource/"):
    print("======================PAINTING PICTURE=======================")
    data = pandas.read_excel(RESOURCE_ROOT + 'book_data.xls')
    number = data['number']
    star = data['star']
    reader = data['reader']
    date = data['date']
    price = data['price']

    # 评分星级与阅读人数
    plt.figure(figsize=(16, 8), dpi=80)
    plt.subplot(111)
    plt.plot(number, star, color='blue', linewidth=3, linestyle='solid', label='star')
    plt.legend(loc='upper right', fontsize=20)
    plt.twinx()
    plt.bar(number, reader, color='gray', label='readers')
    plt.legend(loc='upper left', fontsize=20)
    plt.show()

    # 书籍价格与阅读人数
    plt.figure(figsize=(16, 8), dpi=80)
    plt.plot(number, price, color='purple', label='price')
    plt.legend(loc='upper right', fontsize=20)
    plt.twinx()
    plt.bar(number, reader, color='gray', label='readers')
    plt.legend(loc='upper left', fontsize=20)
    plt.show()

    # 出版时间与阅读人数
    plt.figure(figsize=(16, 8), dpi=80)
    plt.plot(number, date, color='pink', linewidth=3, linestyle='solid', label='date')
    plt.legend(loc='upper right', fontsize=20)
    plt.twinx()
    plt.bar(number, reader, color='gray', label='readers')
    plt.legend(loc='upper left', fontsize=20)
    plt.show()

    # 热力图展示数据间的相关性
    plt.subplots(figsize=(16, 16))
    a = data.iloc[:, [3, 5, 6, 7]].corr()
    sns.heatmap(a, annot=True, vmax=1, square=True, cmap="Blues")
    plt.show()

    # 着重分析散点图
    plt.figure(figsize=(16, 16))  # 图片像素大小
    plt.scatter(star, price, color="green")  # 散点图绘制
    plt.grid()  # 显示网格线
    plt.show()


def parse_number(target):
    res = ''
    for i in range(len(target)):
        if '0' <= target[i] <= '9':
            res += target[i]
    return res.strip()


def parse_float(target):
    res = ''
    for i in range(len(target)):
        if '0' <= target[i] <= '9':
            res += target[i]
        else:
            if res == '' or target[i] != '.':
                pass
            else:
                res += target[i]
    return res


def is_date(target):
    patten_1 = re.compile(r'\d+-\d+')
    patten_2 = re.compile(r'\d+-\d+-\d+')
    if re.match(patten_1, target) or re.match(patten_2, target):
        return True
    return False


def parse_multi_price(target):
    price = lower_price(target)
    return price


def lower_price(target):
    patten_1 = re.compile(r'\d+\.\d+')
    patten_2 = re.compile(r'\d+')
    target_list = target.strip().split('/')
    min_price = 1000000.00
    for item in target_list:
        if re.match(patten_1, item.strip()) or (re.match(patten_2, item.strip()) and not is_date(item.strip())):
            price = parse_float(item.strip())
            if float(price) < min_price:
                min_price = float(price)
    return str(min_price)


def parse_multi_date(target):
    target_list = target.split('/')
    for item in target_list:
        if is_date(item.strip()):
            item = format_date(item)
            return parse_date(item.strip())


def format_date(target):
    target_list = target.strip().split('-')
    res = target_list[0]+'-'+target_list[1]
    return res


def parse_date(target):
    res = ''
    for i in range(len(target)):
        if '1' <= target[i] <= '9':
            res += target[i]
        else:
            if target[i] == '0':
                if res[len(res) - 1] == '.':
                    pass
                else:
                    res += '0'
            else:
                if res == '' or target[i] != '-':
                    pass
                else:
                    res += '.'
    return res


def parse_price_and_date(target):
    price = parse_multi_price(target)
    date = parse_multi_date(target)
    res_list = {'price': price, 'date': date}
    return res_list


class Util:
    pass
