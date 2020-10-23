import requests
from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
from lxml import html
import ftfy #to fix text
import re 

sentences = []

def get_urls():
    # Source to get data 
    BASE_URL = 'https://fangj.github.io/friends/'


    base_page = requests.get(BASE_URL)
    tree = html.fromstring(base_page.content)


    # All urls to scrap
    URLS = [ BASE_URL+href for href in tree.xpath('/html/body/ul/li/a/@href')]

    return URLS



def parse_content(elmts):
    parsed_content = []
    for elmt in elmts:
        content = elmt.text
       
        content = content.replace('\n',' ') # remove new line 
        content = re.sub('\(.*?\)', ' ', content)  #remove text in parenthesis
        content = re.sub('\[].*?\]', ' ', content) #remove line in square bracket
        
        content = ftfy.fix_text(content)
        if len(content.split(':')) == 2:
            key, quote = content.split(':')
            sentences.append((key,quote))





# For each url ,get content of the page 
# get  all <p> elements

def fetch_pages(urls):
    failed_urls = []
    N = len(urls)
    i = 0
    for url in urls:
        try:
            page = requests.get(url)
            status = page.status_code
            if status == 200:
                content = BeautifulSoup(page.content, 'lxml')
                p_elmts = content.find_all('p')
                parse_content(p_elmts)

        except Exception as ex:
            failed_urls.append((i,url))
            print(ex)

        finally:
            i+= 1
            print(f'page {i} on {N} processed')

    
    data = pd.DataFrame(sentences, columns=['actor','quote'])
    data.to_csv('data.csv',sep='\t', header=True, index=False)
    if len(failed_urls) > 0:
        print(failed_urls)

    
urls = get_urls()
fetch_pages(urls)






