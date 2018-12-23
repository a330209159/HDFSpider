__author__ = 'WangYue <admin@lscx.org>'
__date__ = '2018/11/18 9:46'


from bs4 import BeautifulSoup
from GetDateLink import sendHttpRequest


def getPageLink(url):
    """
    获取本日期所有页对应的链接
    :param url:本日期第一页的url
    :return: 返回一个列表，此列表中包含当前日期所有页的链接
    """
    baseURL ='https://www.haodf.com'
    html = sendHttpRequest(url)
    soup = BeautifulSoup(html,'html.parser')
    link = soup.find_all(class_='page_turn_a')
    PageLinkList = []
    PageLinkList.append(url)
    for i in link:
        PageLinkList.append(baseURL+i.get('href'))
    return PageLinkList


def getContentLink(pageurl):
    """
    获取索引页每条问答信息对应的链接
    :param pageurl: 当前页的链接
    :return: 返回一个列表，此列表包含当前页每条问答信息的链接
    """
    html = sendHttpRequest(pageurl)
    soup = BeautifulSoup(html,'html.parser')
    contentlink = soup.find_all(class_= 'hh')
    ContentLinkList= []
    if len(contentlink) == 0:
        for i in range(5):
            contentlink = soup.find_all(class_='hh')
    try:
        for item in contentlink[0].find_all('a'):
            ContentLinkList.append('https:'+item.get('href'))
    except:
        print('获取内容链接发生错误')

    return ContentLinkList

# 测试函数
if __name__ == '__main__':
    for i in getPageLink('https://www.haodf.com/sitemap-zx/20181110_1/'):
        print(i)
