# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from scrapy.cmdline import execute
import os
import sys

def print_hi(name):
    print(f'Hi, {name}')

    if __name__ == '__main__':
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        execute(['scrapy', 'crawl', 'books_item'])


if __name__ == '__main__':
    print_hi('PyCharm')

