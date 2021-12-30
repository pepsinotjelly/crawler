import matplotlib.pyplot as plt
import pandas
import xlrd


def show(RESOURCE_ROOT="./book_request/resource/"):
    data = pandas.read_excel(RESOURCE_ROOT + 'book_data.xls')
    x1 = data['number']
    y1 = data['star']
    y2 = data['reader']
    plt.figure(figsize=(16, 8), dpi=80)
    plt.subplot(111)
    plt.plot(x1, y1, color='blue', linewidth=3, linestyle='solid', label='star')
    plt.legend(loc='upper right', fontsize=20)
    plt.twinx()
    plt.bar(x1, y2, color='gray', label='readers')
    plt.legend(loc='upper left', fontsize=20)
    plt.show()


def parse_number(target):
    res = ''
    for i in range(len(target)):
        if '0' <= target[i] <= '9':
            res += target[i]
    return res.strip()


class Util:
    pass
