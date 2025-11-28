from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()

def getLinks(pageUrl):
    global pages
    
    html = urlopen('http://en.wikipedia.org{}'.format(pageUrl))
    bs = BeautifulSoup(html, 'html.parser')

    try:
        print(bs.h1.get_text())
        print(bs.find(id='mw-content-text').find_all('p')[0].get_text())
        
        edit_link = bs.find(id='ca-edit')
        if edit_link:
            print(edit_link.find('span').find('a').attrs['href'])
    except AttributeError:
        print('This page is missing something! Continuing.')

    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            newPage = link.attrs['href']
            
            if newPage not in pages:
                print('-' * 20)
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)

getLinks('/wiki/Python_(programming_language)')
