import re
import urllib
from pathlib import Path

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
        elif i=="":
            break
        else:
            ss = i.split(': ')
            headers[ss[0]] = ss[1]
    return headers
def spider(title):
    dir=Path('./webpage')
    if not dir.exists():
        dir.mkdir()
    url = 'https://arxiv.org/search/?query=' + title.strip().replace(' ','+') + '&searchtype=all&source=header'
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
            bs.select_one('p.title.is-5').text.strip()
            abs = bs.find('p', 'list-title').a.attrs['href']
            link = bs.find('p', 'list-title').span.find('a').attrs['href']
        print(title, abs, link)
    except:
        print("未找到相关信息\n")
        title = 'unfind'
        abs = None
        link = None

    return {'tilte':title,'abstract link':abs , 'papar link': link}

def get_info():
    list=[]
    data=pd.read_csv('oral.csv')
    for i in range(data.shape[0]):
        print(str(i)+': ')
        title=data['title'][i]
        info=spider(title)
        list.append(info)
        pd.DataFrame(list).to_csv('list.csv')

def download():
    data = pd.read_csv('data.csv')
    for i in range(data.shape[0]):
        print(str(i) + ': ')
        title = data['title'][i]
        url = data['link'][i]


get_info()
