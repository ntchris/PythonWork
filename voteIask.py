
import re
import sys
import time
import json
import string
import gzip
# import urllib2
import urllib
from urllib.request import urlopen
from urllib import request as urlrequest
proxy_host = 'localhost:80'

import random


class Constants:
   LinkBase = u"http://www.iask.ca/plus/digg_ajax.php?action="
   VoteGoodPart = "good"
   VoteBadPart = "bad"
   VoteIdPart = u"&id="
   # SearchKeyword = "onclick=\"postDigg(\'good\',"
   SearchKeyword = "onclick=\"javascript:postDigg('good',"
   RepeatTimes = 45

   
def getVoteActionPart(isVoteGood):
   if(isVoteGood == True):
       return Constants.VoteGoodPart
   else:
       return Constants.VoteBadPart
    
    
def getPageVoteAid(webpage):
   
   
   dontcare, voteid = webpage.decode('utf8').split(Constants.SearchKeyword)
   # print("voteid is  " + voteid)
   
   voteid, dontcare = voteid.split(")\">", 1)
   return voteid

       
def generateVoteUrl(isVoteGood, voteId):
    voteGoodOrBadPart = getVoteActionPart(isVoteGood)
    url = Constants.LinkBase + voteGoodOrBadPart + Constants.VoteIdPart + str(voteId)
    return url



def getHttpHeaders():
    headers={}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"
    accept ="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    headers['Accept'] = accept 

    encode = "gzip, deflate"
    headers['Accept-Encoding'] = encode
    return headers

def readUseProxy(url, proxy):
    headers = getHttpHeaders()
    req = urllib.request.Request(url, data=None, headers=  headers)
    req.set_proxy(proxy_host, 'http')
    resp = urlrequest.urlopen(req)
    page = resp.read( ) 
    return page



def getWebPage(url):   

   # headers is a dict
   headers = getHttpHeaders()
   page = ""
   # page = readUseProxy(url, "127.0.0.1")
   req = urllib.request.Request(url, data=None, headers=  headers)   
   resp = urlrequest.urlopen(req)
   page = resp.read( ) 

   encoding = resp.info().get('Content-Encoding')

   if encoding == 'gzip':
      print("gzip html")
      page = gzip.decompress(page )
   elif encoding  == "deflate":
      print("plain text, deflate")

   return page


def repeatVote(url, times):
    print("working...")
    for i in range(times):
       resp = urlopen(url)
       print(str(i) + " ")
       # sleepSecond = random.uniform(0.5, 6, 0.1)
       sleepSecond = random.randrange(500, 4000, 250) / 1000.0

       print("sleeping for " + str(sleepSecond) + " second")
       time.sleep(sleepSecond)


def main():

   # if len(sys.argv) < 2:
   #   print("Usage: python " + sys.argv[0] + "iask_link")
      # sys.exit(0)

   #webpageUrl = "http://www.iask.ca/news/canada/2020/02/554182.html"
   webpageUrl = input('paste your iask url')
   webpageUrl = webpageUrl.strip()
   
   isvotegood = input("Vote Good or Bad ? ")
   isvotegood = isvotegood.lower()
    
   if(isvotegood == "good"):
      isvotegood = True
   else:
      isvotegood = False
   
   print ("Is to vote Good or Up: " + str(isvotegood))

   # iask_link = sys.argv[1]
   webpage = getWebPage(webpageUrl)
   # print(webpage)

   voteid = getPageVoteAid(webpage)
   
   repeatVoteUrl = generateVoteUrl(isvotegood, voteid)
   print(repeatVoteUrl) 
   
   repeatVote(repeatVoteUrl, Constants.RepeatTimes)

   
main()


