
import re
import sys
import time
import json
import string
import urllib2


class Constants:
   LinkBase = u"http://www.iask.ca/plus/digg_ajax.php?action="
   VoteGoodPart = "good"
   VoteBadPart = "bad"
   VoteIdPart = u"&id="
   # SearchKeyword = "onclick=\"postDigg(\'good\',"
   SearchKeyword = "onclick=\"javascript:postDigg('good',"
   RepeatTimes = 20

   
def getVoteActionPart(isVoteGood):
   if(isVoteGood == True):
       return Constants.VoteGoodPart
   else:
       return Constants.VoteBadPart
    
    
def getPageVoteAid(webpage):
   # print(webpage)
   dontcare, voteid = webpage.split(Constants.SearchKeyword)
   # print("voteid is  " + voteid)

   voteid, dontcare = voteid.split(")\">", 1)
   return voteid

       
def generateVoteUrl(isVoteGood, voteId):
    voteGoodOrBadPart = getVoteActionPart(isVoteGood)
    url = Constants.LinkBase + voteGoodOrBadPart + Constants.VoteIdPart + str(voteId)
    return url


def getWebPage(url):

#   urllib.request.urlopen(url)
   resp = urllib2.urlopen(url)
   page = resp.read()
   return page


def repeatVote(url, times):
    print("working...")
    for i in range(times):
       resp = urllib2.urlopen(url)
       print(str(i) + " ")
       time.sleep(1)


def main():

   # if len(sys.argv) < 2:
   #   print("Usage: python " + sys.argv[0] + "iask_link")
      # sys.exit(0)

   webpageUrl = "http://www.iask.ca/news/canada/2018/07/492898.html"
   webpageUrl = raw_input('paste your iask url')
   webpageUrl = webpageUrl.strip()
   
   isvotegood = raw_input("Vote Good or Bad ? ")
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
   # working link  http://www.iask.ca/plus/digg_ajax.php?action=bad&id=492898
   
   repeatVote(repeatVoteUrl, Constants.RepeatTimes)

   
main()


