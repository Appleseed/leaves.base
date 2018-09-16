import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
import requests

def getKeywords(nlpUserName, nlpPass, url,rel=0,lim=3):
        natural_language_understanding = NaturalLanguageUnderstandingV1(username=nlpUserName, password=nlpPass, version='2018-03-16')
        response = natural_language_understanding.analyze( url=url, features=Features( keywords=KeywordsOptions( emotion=False, sentiment=False, limit=lim)))
        return [i['text'] for i in response['keywords'] if i['relevance'] > rel]

def getTags(nlpUserName, nlpPass, url, rel=0, lim=3):
    try:
       keywords = ''.join(getKeywords(nlpUserName, nlpPass, url, rel, lim))
       return keywords
    except Exception as e:
       print("Error ", str(e))

#print (getTags("c5c2dd2d-b29b-4268-9748-dfd19687e5c7", "PotmceYly2BB", "https://github.com/sindresorhus/awesome-nodejs"))
