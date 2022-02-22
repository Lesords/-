import datetime
import xlwt

import requests
import json
import re
from bs4 import BeautifulSoup

header = {  # 请求头
    'Referer': "https://music.163.com/",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}


def get_html(url):  # 获取url的网页内容
    # return requests.get(url,headers=header).text  # 简单版
    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def get_info(html): # 获取json数据
    # soup = BeautifulSoup(html, "lxml") # lxml格式解析html
    # # 获取对应的json数据
    # 如果内容里有<字符，会使数据不全
    # info = soup.find('textarea',attrs={'id':'song-list-pre-data'}).string
    # # info = soup.select('textarea[id="song-list-pre-data"]')[0].string  # 方法二
    pattern = r'<textarea .*>.*</textarea>'     # 找到对应json文件
    info = re.findall(pattern, html)[0]
    pat_head = re.compile('<textarea id="song-list-pre-data" style="display:none;">')
    pat_tail = re.compile("</textarea>")
    info = re.sub(pat_head, '', info)
    info = re.sub(pat_tail, '', info)
    return info


def crawl(url, file_name):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("爬虫结果")
    info = ['排名', '歌曲', '歌手']
    for index, val in enumerate(info):
        sheet.write(0, index, val)

    html = get_html(url)
    print("正在crawling --- ", file_name)
    # 保存html，方便判断对应数据的位置
    # with open("debug\\html_content.html", 'w', encoding='utf-8') as fp:
    #     fp.write(html)

    # print(html)   # 输出html
    datas = get_info(html)      # 获取json数据
    # print(datas)
    datas = json.loads(datas)   # 解析成python对象
    # print(datas[0])
    info = []                   # 保存最终的数据
    rank = 1                    # 歌曲排名
    for data in datas:
        music = data['name']           # 获取歌名
        singer = ""
        flag = 0
        for val in data['artists']:
            singer += ('/' if flag == 1 else '') + val['name']
            flag = 1

        info.append({'排名': rank, '歌名': music, '歌手': singer}) # 添加数据
        sheet.write(rank, 0, rank)
        sheet.write(rank, 1, music)
        sheet.write(rank, 2, singer)
        rank += 1                               # 排名++

    workbook.save('data\\'+file_name)


if __name__ == '__main__':
    url = "https://music.163.com/discover/toplist?id="
    lists = ['19723756', '3779629', '2884035', '3778678']  # 飙升榜、新歌榜、原创榜、热歌榜
    name = ['飙升榜', '新歌榜', '原创榜', '热歌榜']

    today = datetime.datetime.now()
    today = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
    pos = 0
    crawl(url+lists[pos], name[pos]+" "+today+".xls")