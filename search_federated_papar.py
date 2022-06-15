# -*- coding: UTF-8 -*-
"""
@author:aaaal
@file:search.py.py
@time:2021/10/12
"""
import re
import urllib

import pandas as pd
from bs4 import BeautifulSoup
import pandas
from pathlib import Path
name=['CVPR_2021','CVPR_2020','ICCV_2021','ICCV_2019']
for n in name:
    data = pd.read_csv(n+'.csv')
    list = []
    for i in range(data.shape[0]):
        if "ederated" in data['title'][i]:
            list.append({"title": data['title'][i], "abstract": data['abstract'][i], "keyword": "federated in title"})

    for i in range(data.shape[0]):
        if "ederated" in data['abstract'][i]:
            list.append(
                {"title": data['title'][i], "abstract": data['abstract'][i], "keyword": "federated in abstract"})

    for i in range(data.shape[0]):
        if "ecentral" in data['title'][i]:
            list.append(
                {"title": data['title'][i], "abstract": data['abstract'][i], "keyword": "decentralized in title"})

    for i in range(data.shape[0]):
        if "ecentral" in data['abstract'][i]:
            list.append(
                {"title": data['title'][i], "abstract": data['abstract'][i], "keyword": "decentralized in abstract"})

    for i in range(data.shape[0]):
        if "istributed" in data['title'][i]:
            list.append({"title": data['title'][i], "abstract": data['abstract'][i], "keyword": "istributed in title"})

    for i in range(data.shape[0]):
        if "istributed" in data['abstract'][i]:
            list.append(
                {"title": data['title'][i], "abstract": data['abstract'][i], "keyword": "istributed in abstract"})
    list2 = []
    s = set()
    for i in list:
        if i['title'] not in s:
            list2.append(i)
            s.add(i['title'])
    pandas.DataFrame(list2).to_csv(n+'_FL.csv')
