__author__ = 'WangYue <admin@lscx.org>'
__date__ = '2018/11/18 9:46'


from bs4 import BeautifulSoup
from GetDateLink import sendHttpRequest


def getPageLink(url):
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


if __name__ == '__main__':
    for i in getPageLink('https://www.haodf.com/sitemap-zx/20181110_1/'):
        print(i)
