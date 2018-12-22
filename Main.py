__author__ = 'WangYue <admin@lscx.org>'
__date__ = '2018/11/18 13:54'

from GetContent import *
from GetDateLink import searchPage, getLinkList
from GetContentLink import getPageLink, getContentLink
import time
import random
import datetime
import sys
import getopt
# test

def crawl_1607052433(startdate, enddate):
    crawSub(startdate,enddate)


def crawSub(startdate,enddate,pagenum=0,eachnum=0,rfbp=0):
    linkmap = searchPage()
    dateStrList = getLinkList(startdate, enddate)

    for k in dateStrList:
        print('Processing -> ' + k + ' ',end=' ')
        pagelink = getPageLink(linkmap[k])  # 页数链接

        total = pagenum*500
        failedtimes = 1
        lastfailed = -1
        pagelength = len(pagelink)
        if pagelength == 0:
            for i in range(2):
                pagelink = getPageLink(linkmap[k])
        flag=0
        if rfbp == 1:
            flag = 1
        time.sleep(5)
        print('本日总页数:{}'.format(pagelength))
        for page in range(pagenum, pagelength):
            print('正在处理第{}页,网址 {}'.format(page + 1, pagelink[page]))
            if flag == 1:
                each = eachnum
            else:
                each = 0
            contentlink = getContentLink(pagelink[page])
            time.sleep(5)
            while True:
                sleeptime = random.randint(1, 3)
                try:
                    if each == len(contentlink):
                        break
                    export2Json(k, total + each, getContent(contentlink[each]))
                    each += 1
                    if each % 3 == 0:
                        time.sleep(sleeptime)
                    failedtimes = 1
                except:
                    if lastfailed == each:
                        failedtimes += 1
                    if failedtimes >= 3:
                        print(str(total + each) + '尝试三次不成功，自动跳转到下一个...')
                        each += 1
                        failedtimes = 1
                        lastfailed = each
                        continue
                    print('[{}]'.format(str(time.strftime("%H:%M:%S", time.localtime()))),end=' ')
                    print(str(total + each) + '号文件爬取不成功\n网址:' + contentlink[each])
                    print('失败次数:{}'.format(failedtimes),end=' ')
                    print('5s后重新爬取...')
                    lastfailed = each
                    time.sleep(5)
            total += each
            time.sleep(20)
            flag = 0


def rfbp(lastnum, date):
    """
    resume from break-point
    """
    page = int(lastnum / 500)
    num = int(lastnum % 500)
    print('断点续爬 -> 页数:{},内容号数:{}'.format(page+1,num))
    startdate = datetime.datetime.strptime(date, '%Y%m%d')
    lastday = startdate - datetime.timedelta(days=1)
    lastDayStr = lastday.strftime('%Y%m%d')
    crawSub(lastDayStr,date,page,num,1)


def cmdprocess(argv):

    date =''
    num = -1
    try:
        opts, args = getopt.getopt(argv, "hrd:n:", ["resume", "date=","num="])
    except getopt.GetoptError:
        print('Main.py -r -d <date> -n <lastnum>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Main.py -r -d <date> -n <lastnum>')
            sys.exit()
        elif opt in ("-r", "--resume"):
            for opt, arg in opts:
                if opt in ('--date','-d'):
                    date = arg
                elif opt in ('--num','-n'):
                    num = int(arg)
    if len(date)>0 and num != -1:
        rfbp(num,date)
        return
    print('usage:Main.py -r -d <date> -n <lastnum>')


if __name__ == '__main__':
    cmdprocess(sys.argv[1:])