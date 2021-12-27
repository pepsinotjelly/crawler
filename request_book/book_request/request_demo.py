import urllib.error
import http.cookiejar
from urllib.request import Request, urlopen


def request_maker(page):
    origin_url = "https://book.douban.com/top250"
    header = {'User-Agent': 'Mozilla/5.0',
              'Referer': 'https://book.douban.com/',
              }
    form_data = {
        'start': page
    }
    data = urllib.parse.urlencode(form_data)
    url = origin_url + '?' + data
    request = Request(url, headers=header)
    return request


def cookie_maker(request):
    filename = './cookie.txt'
    cookie = http.cookiejar.LWPCookieJar(filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open(request)
    cookie.save(ignore_discard=True, ignore_expires=True)


def cookie_reader(url):
    cookie = http.cookiejar.LWPCookieJar()
    cookie.load('./cookie.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open(url)
    return response


def do_request(is_write, page):
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
    # 构造请求
    request = request_maker(page)
    # 配置全局opener
    urllib.request.install_opener(opener)
    try:
        response = urlopen(request)
        html = response.read()
        f = open("./book_response/bookList_" + str(page) + ".html", "wb")
        if is_write:
            f.write(html)
        f.close
        print(response.geturl())
        print(response.getcode())
        print(response.info())
        response.close()
    except urllib.error.HTTPError as e:
        print(e.reason)
        print(e.code)
        print(e.headers)


page = 0
do_is_write = False  # 是否重写本地文件,True时重写本地.html文件，false时跳过。
for i in range(10):
    page = i * 25
    do_request(do_is_write, page)

