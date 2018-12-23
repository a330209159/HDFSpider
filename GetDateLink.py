__author__ = 'WangYue <admin@lscx.org>'
__date__ = '2018/11/17 15:58'
import datetime
import requests
import random
from bs4 import BeautifulSoup


def getLinkList(startdateStr, enddateStr):
    """
    获取指定日期段内的链接列表
    :param startdateStr: 开始日期
    :param enddateStr: 结束日期
    :return: 返回一个指定日期内的链接列表
    """
    enddate = datetime.datetime.strptime(enddateStr, '%Y%m%d')
    startdate = datetime.datetime.strptime(startdateStr, '%Y%m%d')
    nextday = startdate
    datelist = []
    while True:
        nextday = nextday + datetime.timedelta(days=1)
        datelist.append(nextday.strftime('[%Y-%m-%d]'))
        if nextday.strftime('%Y-%m-%d') == enddate.strftime('%Y-%m-%d'):
            break
    return datelist


def getUserAgent():
    """
    从列表里随机获取一个UserAgent，避免被系统判为爬虫，同时构造headers
    :return: 直接返回构造好的headers
    """
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"
    ]
    spider_agent_list = [
        'Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
    ]
    headers = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': random.choice(spider_agent_list),
               'Connection': 'keep-alive',
               'Referer': 'https://www.haodf.com/'
               }
    return headers


def searchPage():
    """
    爬取当前年所有日期对应的链接
    :return:返回一个字典，key是日期，而value是日期对应的链接
    """
    url = 'https://www.haodf.com/sitemap-zx/2018/'
    html = sendHttpRequest(url)
    soup = BeautifulSoup(html, 'html.parser')
    linkmap = {}
    for item in soup.find_all('a'):
        linkmap[item.text] = 'https:' + item.get('href')
    return linkmap


def sendHttpRequest(url):
    """
    调用requests库请求html网页
    :param url: 要请求的网址
    :return: 返回html源码
    """
    headers = getUserAgent()
    try:
        html = requests.get(url, headers=headers, timeout=15).text
    except:
        print('获取网页超时')
    return html

# 本模块测试函数
if __name__ == '__main__':
    linkmap = searchPage()
    dateStrList = getLinkList('20180930', '20181003')
    for k in dateStrList:
        print(k, linkmap[k])
