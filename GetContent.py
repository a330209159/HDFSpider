__author__ = 'WangYue <admin@lscx.org>'
__date__ = '2018/11/18 10:22'
from GetDateLink import sendHttpRequest
from bs4 import BeautifulSoup
import json
import os


def getContent(url):
    """
    负责爬取问答信息内容，并构造json格式的函数
    :param url: 要爬取的问答页的链接
    :return: 返回一个字典，此字典中包含此问答页的问答内容
    """
    html = sendHttpRequest(url)
    soup = BeautifulSoup(html, 'html.parser')

    c_des = ''
    c_ques = []
    c_ans = []
    c_total = dict()

    content = soup.find_all(class_='stream_left_content fl')[0]
    title = content.find_all(class_='fl-title ellps')[0].get_text()
    allwarp = content.find_all(class_=['f-c-r-wrap'])
    description = allwarp[0].find_all(class_=['f-c-r-w-subtitle', 'f-c-r-w-text'])

    for i in description:
        c_des += i.get_text() + '\n'
    for i in range(1, len(allwarp)):
        # print(allwarp[i].find_all(class_ =['f-c-r-doctext','f-c-r-w-text'])[0].get_text().replace('\n','').strip())
        patient = allwarp[i].find_all(class_='f-c-r-w-text')
        doctor = allwarp[i].find_all(class_='f-c-r-doctext')
        if len(patient) != 0:
            c_ques.append(patient[0].get_text().replace('\n', '').strip() + ' ')

        if len(doctor) != 0:
            c_ans.append(doctor[0].get_text().replace('\n', '').strip() + ' ')
    c_total['title'] = title
    c_total['description'] = c_des
    c_total['question'] = c_ques
    c_total['answer'] = c_ans

    return c_total


def export2Json(dictpath, fileid, content):
    """
    将页面内容提取到json中的函数
    :param dictpath: 要提取json文件到的目录
    :param fileid: 页面的id号
    :param content: 包含页面内容的字典
    """
    if not os.path.exists(dictpath):
        os.mkdir(dictpath)
    with open('{}/{}.json'.format(dictpath, fileid), 'w', encoding='utf-8') as fout:
        json.dump(content, fout, ensure_ascii=False, indent=4)

# 用于测试本模块的函数
if __name__ == '__main__':
    content = getContent(url='https://www.haodf.com/doctorteam/flow_team_6463903072.htm')
    export2Json(content)
