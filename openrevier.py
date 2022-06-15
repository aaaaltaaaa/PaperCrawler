import re
import urllib
from bs4 import BeautifulSoup
import pandas
from pathlib import Path
# 显示'.asd '为class=3D"asd" 最后需要搜索class:3D:asd
list = []
for i in range(0, 1):
    with open("NeurIPS.mhtml", 'rb+') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        items = soup.find_all('li', attrs={'class': 'note'})
        for i, item in enumerate(items):
            info={}
            info['title'] = item.a.text.strip()
            details= item.select('div>div>ul>li')
            for j in range(len(details)):
                info[details[j].text.strip().split(":")[0].strip()]= details[j].text.strip().split(":")[1].strip()
            if len(details) != 3:
                print(i)
            info['openrevier_link'] = item.a.attrs['href']
            list.append(info)
            print(i, list[-1])
            if i % 100 == 99:
                pandas.DataFrame(list).to_csv('data.csv', encoding='utf-8-sig')
        else:
            pandas.DataFrame(list).to_csv('data.csv', encoding='utf-8-sig')
pass
import re
import urllib
from pathlib import Path
from difflib import SequenceMatcher
import pandas as pd
from bs4 import BeautifulSoup
import os


def head(filename):
    ss = open(filename)
    ss = ss.read()
    ss = ss.split('\n')
    headers = {}
    for i in ss:
        if 'Accept-Encoding' in i or 'accept-encoding' in i:
            pass
        elif i == "":
            break
        else:
            ss = i.split(': ')
            headers[ss[0]] = ss[1]
    return headers


def spider(title):
    dir = Path('./webpage')
    if not dir.exists():
        dir.mkdir()
    url = 'https://arxiv.org/search/?query=' + title.strip().replace(' ', '+') + '&searchtype=all&source=header'
    # headers = head('head.txt')
    # req = urllib.request.Request(url=url, headers=headers, method="POST")
    try:
        response = urllib.request.urlopen(url)
        bs = BeautifulSoup(response.read().decode('utf-8'), 'html.parser')
        path = open('./webpage/' + title, 'wb')
        path.write(response.read())
        path.close()
    except:
        print("网络故障,未找到相关信息\n")
        title = 'unfind'
        abs = None
        link = None
    try:
        if not bs.select_one('p.title.is-5'):
            title = 'unfind'
            abs = None
            link = None
        else:
            origin_title = title
            title = bs.select_one('p.title.is-5').text.strip()
            abs = bs.find('p', 'list-title').a.attrs['href']
            link = bs.find('p', 'list-title').span.find('a').attrs['href']
            if similarity(origin_title, title) < 0.8:
                print(similarity(origin_title, title))
                raise
        print(origin_title, title, abs, link)

    except:
        print("未找到相关信息\n")
        title = 'unfind'
        abs = None
        link = None

    return {'title': title, 'abstract link': abs, 'pdf link': link}


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def get_info():
    list = []
    data = pd.read_csv('data.csv')
    data['abstract link']=None
    data['pdf link']=None
    for i in range(data.shape[0]):
        print(str(i) + ': ')
        title = data['title'][i]
        info = spider(title)
        if info['title']!='unfind':
            data['abstract link'][i]=info['abstract link']
            data['pdf link'][i]=info['pdf link']
        list.append(info)
        # pd.DataFrame(list).to_csv('list.csv', encoding='utf-8-sig')
        pd.DataFrame(data).to_csv('data.csv', encoding='utf-8-sig')


def download():
    data = pd.read_csv('data.csv')
    for i in range(data.shape[0]):
        print(str(i) + ': ')
        title = data['title'][i]
        url = data['link'][i]


get_info()
