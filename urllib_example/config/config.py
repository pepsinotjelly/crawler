USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/96.0.4664.110 Safari/537.36 '
# 如果豆瓣把IP封了就在HEADER里加一个新鲜的Cookie
HEADER = {
    'User-Agent': USER_AGENT,
    'Referer': 'https://book.douban.com/top250'
    # ,'Cookie': 'bid=fLAdqpnsfRE; __utmc=30149280; __utmc=81379588; '
    #           '__utmz=30149280.1640321301.3.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; '
    #           '__utmz=81379588.1640321301.3.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; '
    #           'push_noty_num=0; push_doumail_num=0; dbcl2="247235182:DmC9SsZ2iE4"; ck=0Tux; __utmv=30149280.24723; '
    #           '_pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1640579448%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; '
    #           '_pk_ses.100001.3ac3=*; ap_v=0,6.0; __utma=30149280.1503170269.1640066250.1640321301.1640579448.4; '
    #           '__utma=81379588.95857263.1640066250.1640321301.1640579448.4; __utmb=30149280.2.10.1640579448; '
    #           '__utmb=81379588.2.10.1640579448; '
    #           '_pk_id.100001.3ac3=021988dc59405135.1640066250.4.1640579466.1640324096. '
}
RESOURCE_PATH = './book_request/resource/'