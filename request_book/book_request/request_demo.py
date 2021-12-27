import re
import urllib.error
import http.cookiejar
from urllib.request import Request, urlopen

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36',
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


def cookie_maker(request):
    filename = RESOURCE_PATH + '/cookie.txt'
    cookie = http.cookiejar.LWPCookieJar(filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open(request)
    cookie.save(ignore_discard=True, ignore_expires=True)


def cookie_reader(url):
    cookie = http.cookiejar.LWPCookieJar()
    cookie.load(RESOURCE_PATH + '/cookie.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open(url)
    return response


def picture_reader(data, page):
    patten = r'https://img[0-9].doubanio.com/view/subject/s/public/s[0-9]{7}.jpg|https://img[0-9].doubanio.com/view/subject/s/public/s[0-9]{8}.jpg2'
    pat = re.compile(patten)
    img_urls = re.findall(pat, str(data))
    print(img_urls)
    print(len(img_urls))
    for img in range(len(img_urls)):
        print("第%d张图片地址：%s" % (img, img_urls[img]))
        print("开始下载第%d张。。。" % img)
        urllib.request.urlretrieve(img_urls[img], RESOURCE_PATH+"book_img/img_" + str(page) + "_" + str(img)+".jpg")
        print("下载成功\n======================")


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


def use_cookie(is_write, page):
    request = request_demo(page)
    cookie_maker(request)
    cookie = http.cookiejar.LWPCookieJar()
    cookie.load(RESOURCE_PATH+'cookie.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = opener.open(url_maker(page))
    return response


def use_demo(is_write, page):
    request = request_demo(page)
    try:
        response = urlopen(request)
        html = response.read()
        if is_write:
            f = open(RESOURCE_PATH+"book_response/bookList_" + str(page) + ".html", "wb")
            f.write(html)
            f.close
        picture_reader(html, page)
        print(response.geturl())
        print(response.getcode())
        print(response.info())
        response.close()
    except urllib.error.HTTPError as e:
        print(e.reason)
        print(e.code)
        print(e.headers)


def do_request(is_write, if_cookie, if_proxy):
    page = 0
    for i in range(10):
        page = i * 25
        if if_proxy:
            use_proxy(is_write, page)
        elif if_cookie:
            use_cookie(is_write, page)
        else:
            use_demo(is_write, page)


# do_write = False  # 是否重写本地文件,True时重写本地.html文件，False时跳过。
# if_use_cookie = False  # 是否创造cookie，True时重写本地cookie.txt文件，False时跳过。
# if_use_proxy = False

