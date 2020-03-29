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
pd.options.display.max_rows = 100

url = ['http://www.livesinabox.com/friends/season1/102towsg.htm',\
       'http://www.livesinabox.com/friends/season1/103thumb.htm']
    
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
print(complete_data.head(10))
print(complete_data.Actor.value_counts())

print(complete_data.shape)