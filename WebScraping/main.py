#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 18:40:56 2020

@author: giorgiomondauto
"""
import requests
from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
from lxml import html


pd.options.display.max_rows = 100

# url = ['http://www.livesinabox.com/friends/season1/101pilot.htm', 'http://www.livesinabox.com/friends/season1/102towsg.htm',
#         'http://www.livesinabox.com/friends/season1/103thumb.htm','http://www.livesinabox.com/friends/season1/104towgs.htm',
#        'http://www.livesinabox.com/friends/season1/105egld.htm','http://www.livesinabox.com/friends/season1/106butt.htm',
#        'http://www.livesinabox.com/friends/season1/107towbo.htm','http://www.livesinabox.com/friends/season1/108ndt.htm',
#        'http://www.livesinabox.com/friends/season1/109uga.htm','http://www.livesinabox.com/friends/season1/110monk.htm',
#        'http://www.livesinabox.com/friends/season1/111mbing.htm','http://www.livesinabox.com/friends/season1/112towdl.htm',
#        'http://www.livesinabox.com/friends/season1/113tits.htm','http://www.livesinabox.com/friends/season1/114towch.htm']
#         # 'http://www.livesinabox.com/friends/season1/115towsg.htm','http://www.livesinabox.com/friends/season1/116part1.htm',
#         # 'http://www.livesinabox.com/friends/season1/117part2.htm','http://www.livesinabox.com/friends/season1/118poke.htm',
#         # 'http://www.livesinabox.com/friends/season1/119mga.htm','http://www.livesinabox.com/friends/season1/120toweo.htm',
#         # 'http://www.livesinabox.com/friends/season1/121towfm.htm','http://www.livesinabox.com/friends/season1/122ick.htm',
#         # 'http://www.livesinabox.com/friends/season1/123birth.htm','http://www.livesinabox.com/friends/season1/124rafo.htm']


def get_urls():
    # Source to get data 
    BASE_URL = 'https://fangj.github.io/friends/'


    base_page = requests.get(BASE_URL)
    tree = html.fromstring(base_page.content)


    # All urls to scrap
    URLS = [ BASE_URL+href for href in tree.xpath('/html/body/ul/li/a/@href')]

    return URLS

url = get_urls()

complete_script = []
for URL in url:
    
    response = get(URL)
        
    html_soup = BeautifulSoup(response.text, 'html.parser')
    movie_containers = html_soup.find_all('p')
    movie_containers
    
    paragraphs = []
    for x in movie_containers:
        paragraphs.append(str(x))
        
    paragraphs = ','.join(paragraphs)
    
    
    dialogs = ','.join(paragraphs.split('</b>')).replace('\n',' ')
    dialogs = dialogs.split('><b>')
    sep = '</p>'
    
    test = [re.split(sep, text.replace('<font color="#0000FF">',''))[0] for text in dialogs][2:]
    dataframe = []
    for i in test:
        dataframe.append(pd.Series(i))
    
    data = pd.DataFrame(pd.concat(dataframe, axis = 0),columns = ['Script'])
    data = pd.DataFrame(data.Script.str.split(':,',1).tolist(), columns = ['Actor','Script'])
    data.head()
    (data.Script =='').value_counts()
    data = data[data.Script !='']
    data.Actor.value_counts()
    data = data.drop_duplicates(['Actor','Script'],keep = 'first')
    main_actors = 'Ross|Monica|Rachel|Chandler|Phoebe|Joey|All'
    data = data[data.Actor.str.contains(main_actors)]
    complete_script.append(data)
    
complete_data = pd.concat(complete_script,axis = 0)
complete_data.Script = complete_data.Script.apply(lambda x: str(x).replace('</font>',''))
complete_data.Actor =complete_data.Actor.replace('<b>All','All')
complete_data.to_csv('data_main.csv',sep='\t', header=True, index=False)


print(complete_data.head(10))
print(complete_data.Actor.value_counts())

print(complete_data.shape)