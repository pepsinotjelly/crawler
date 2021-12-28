# -*- coding: UTF-8 -*-
"""
@Project ：crawler 
@File    ：main.py
@Author  ：Sonia.Suen
@Date    ：2021/12/14 11:11 PM 
"""
from scrapy.cmdline import execute
import os
import sys


def print_hi(name):
    print(f'Hi, {name}')

    if __name__ == '__main__':
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        execute(['scrapy', 'crawl', 'books_item'])


if __name__ == '__main__':
    print_hi('Spider!')