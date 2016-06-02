import urllib2
import re
import sys
import httplib
import requests
import pprint
import string
import urllib
import urlparse
from bs4 import BeautifulSoup,SoupStrainer

wiki="https://docs.python.org/3.4/"

myurl=[]
myurls=[]
list_urls=[]
urls=[]


response = requests.get(wiki)
page = BeautifulSoup(response.content,"html.parser")
page=str(page)



def getURL(page):
    """

    :param page: html of web page (here: Python home page) 
    :return: urls in that page 
    """
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote

def urls(page):
    while True:
        url, n = getURL(page)
        page = page[n:]
        if url:
            list_urls.append(url)
        else:
            break
    return list_urls

    


def expand_url(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc,timeout=10)
    resource = parsed.path
    if parsed.query != "":
        resource += "?" + parsed.query
    h.request('HEAD', resource )
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    elif response.status/100 == 2:
        return url
    else:
        return False

def add_true_links(page):
    link=[]
    myurl=urls(page)
    for url in myurl:
        url_value=expand_url(url)
        if url_value:
            link.append(url)
            
    return link
    
    
    

pprint.pprint (add_true_links(page))
          





