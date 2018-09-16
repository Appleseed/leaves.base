import os
import urllib.request

try:
    host = os.environ["LEAVES_API_URL"]
except:
    host = 'http://206.189.143.212:8081'

def req(link):
    f = urllib.request.urlopen(link)
    myfile = f.read()
    return myfile.decode("utf-8")

def content_full(url):
    link = host + "/content/full?url=" + url
    myfile = req(link)
    return myfile

def content_raw(url):
    link = host + "/content/raw?url=" + url
    myfile = req(link)
    return myfile

def content_read(url):
    link = host + "/content/read?url=" + url
    myfile = req(link)
    return myfile

def content_text(url):
    link = host + "/content/text?url=" + url
    myfile = req(link)
    return myfile

def meta_card(url):
    link = host + "/meta/card?url=" + url
    myfile = req(link)
    return myfile

def meta_pagerank(url):
    link = host + "/meta/pagerank?url=" + url
    myfile = req(link)
    return myfile

