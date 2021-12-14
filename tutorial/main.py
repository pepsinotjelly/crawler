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
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

    if __name__ == '__main__':
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        execute(['scrapy', 'crawl', 'books_item'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Sonia')