import urllib.error
from urllib.request import Request, urlopen

origin_url = "https://book.douban.com/top250"
header = {'User-Agent': 'Mozilla/5.0',
          'Referer': 'https://book.douban.com/',
          'Cookie': 'bid=fLAdqpnsfRE; __utmc=30149280; __utmc=81379588; '
                    '_pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1640321301%2C%22https%3A%2F%2Faccounts.douban.com%2F%22'
                    '%5D; _pk_ses.100001.3ac3=*; __utma=30149280.1503170269.1640066250.1640083125.1640321301.3; '
                    '__utmz=30149280.1640321301.3.2.utmcsr=accounts.douban.com|utmccn=('
                    'referral)|utmcmd=referral|utmcct=/; __utma=81379588.95857263.1640066250.1640083125.1640321301.3; '
                    '__utmz=81379588.1640321301.3.2.utmcsr=accounts.douban.com|utmccn=('
                    'referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0; '
                    'dbcl2="247235182:DmC9SsZ2iE4"; ck=0Tux; __utmb=81379588.4.10.1640321301; '
                    '_pk_id.100001.3ac3=021988dc59405135.1640066250.3.1640323617.1640083125.; __utmv=30149280.24723; '
                    '__utmb=30149280.6.10.1640321301 '
          }
page = 0
form_data = {
    'start': page
}
data = urllib.parse.urlencode(form_data)
url = origin_url + '?' + data
request = Request(url, headers=header)
is_write = True  # 是否重写本地文件
try:
    response = urlopen(request)
    print(403)
    html = response.read()  # .decode('UTF-8')
    f = open("./myBook.html", "wb")
    if is_write:
        f.write(html)
    f.close
    print(html)
    print(response.geturl())
    print(response.getcode())
    print(response.info())
    response.close()
except urllib.error.HTTPError as e:
    if e.code == 403:
        print("ERROR:Cookie Expired!")
