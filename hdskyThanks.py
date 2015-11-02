username = 'zzz'
password = 'zz'
MaximumItemToThank = 400
StartingPageSetting = 4
Debug = True
OnLine = True
# always assume an item is NOT thanked already online, do not check the detail page.
SKIPCheckingThankedOnline = True

# sleep for N second between each thank action, N a random value between the min and min +10 sec
SleepMinSec = 20

LoginSuccessKeyWord = "欢迎回来"
DataFileAlreadyThankedItems = "AlreadyThankedItemIDList.txt"

ThankUrlTemplate = 'https://hdsky.me/thanks.php'

ItemDetailUrlTemplate1 = "https://hdsky.me/details.php?id="
ItemDetailUrlTemplate2 = "&amp;hit=1"

ThankedKeyString = ");\" value=\"&nbsp;&nbsp;感谢发布者+3魔力值&nbsp;&nbsp;\" />"
UrlMainPage = "https://hdsky.me/"



#TempFileName = "tempItemListPage"

itemListPageLinkTemplate = "https://hdsky.me/torrents.php?incldead=1&spstate=0&page="



###############################################################################
import urllib
import urllib2
import cookielib
import time
import random
import os
import threading


class Global:
   # define all global var
   AvailabelItemIDList = []
   ToThankItemIDList = []
   AlreadyThankedItemIDList = []
   thankedCountInThisSession = 0
   oldPoint = 0

 

def opLog(logtext):
   print logtext
   return

def debugLog(debugText):
   if (Debug): 
       print debugText


# ====================================================
class MyCheckUserPointThread(threading.Thread):
   def __init__(self, sleepTimeSec = 60):
      threading.Thread.__init__(self)
      self.toStop = False
      self.setDaemon(True)
      self.sleepTime = sleepTimeSec
   
   def requestStop(self):
      self.toStop = True

   def run(self):
      self.toStop = False
      
      while(not self.toStop):        

        if( self.toStop == True):
           return
        time.sleep(self.sleepTime)
        outPutUserPointInfo()







def outPutUserPointInfo():
    newPoint = getUserPointFromUrlOnline(UrlMainPage)
    delta = float(newPoint.replace(",","") ) - Global.oldPoint
    opLog("============================================================")
    opLog("User point is now "+ newPoint + ", gained "+ str(delta) + " Points")
    opLog("============================================================")

def loadDataAlreadyThanked():
   opLog("loading file " + DataFileAlreadyThankedItems)
   if (not os.path.exists(DataFileAlreadyThankedItems)):
      opLog("data file not exist, skip")
      return
   
   f = open(DataFileAlreadyThankedItems, 'r')

   with open(DataFileAlreadyThankedItems, 'rU') as in_file:
       Global.AlreadyThankedItemIDList = in_file.read().split('\n')
   f.close()
   debugLog("list is " + str(Global.AlreadyThankedItemIDList))
      
   return




def updateAlreadyThankedDataFile(newItemId_thanked):
   
   if(Global.AlreadyThankedItemIDList.count(newItemId_thanked)==0):
       opLog("updating local database, adding " + newItemId_thanked)
       Global.AlreadyThankedItemIDList.append(newItemId_thanked)   
       
       #  !!!
       afile = open(DataFileAlreadyThankedItems, 'a+')
       afile.write(newItemId_thanked+"\n")
       afile.close();
   return



def sleepRandom():
   sec = random.randint(SleepMinSec, SleepMinSec+10)
   opLog("Sleeping "+ str(sec)+" sec")
   if(OnLine):
       time.sleep(sec); 
   return

def openLoginPageOnline():
   # cookie
   cj = cookielib.CookieJar()
   opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
   opener.addheaders = [('User-agent', 'FireFox')]
   urllib2.install_opener(opener)


   #url = 'http://hdsky.me/takelogin.php'
   url = 'https://hdsky.me/takelogin.php'
   # 登陆, form action is post
   loginData={}
   loginData['username'] = username
   loginData['password'] = password


   loginUrlValues = urllib.urlencode(loginData)
   #print url
   #print loginUrlValues
   
   req = urllib2.Request(url, loginUrlValues)
   #print req
   response = urllib2.urlopen(req)
   respPage = response.read()
   #欢迎回来, username
   if(respPage.find(LoginSuccessKeyWord)>0 and respPage.find(username)>0 ):
      loginOK=True
   else:
      loginOK=False

   return loginOK


def getWebPageText(url):
   if(OnLine!=True):
       return;

   pageResponse = urllib2.urlopen(url)
   the_page = pageResponse.read()
   if(Debug):
       print the_page
   return the_page


   
def loadMainPageOnline():
   opLog("loading main page ")
   time.sleep(3)
   pageText = getWebPageText("https://hdsky.me/torrents.php")
   #mainPageResponse = urllib2.urlopen("http://hdsky.me/torrents.php")
   #the_page = mainPageResponse.read()
   #print the_page
   return pageText


def loadTestFile(file):
   opLog( "loading test page file " + file )
   f = open(file, 'r')
   fileText = f.read()
   # fileText = unicode(fileText) error
   #fileText = fileText.encode("UTF-8") error
   #fileText = fileText.decode("UTF-8")
   f.close()
   debugLog("file text size is " + str(len(fileText)))
   return fileText


def getValueBetweenStrings(fullPageText, keyStringBefore, keyStringAfter, startingPoint=0):
   
   posi1 = fullPageText.find(keyStringBefore, startingPoint)
   debugLog("posi1 is " + str(posi1 ))
   if(posi1<=0):
      print "ERROR finding posi1 "
      return
   posi2 = fullPageText.find(keyStringAfter, posi1)
   debugLog( "posi2 is " + str(posi2))
   if(posi2<=0):
      print "ERROR finding posi2 " + fullPageText[posi1:]
      return
   
   deltaSkipKeyStringBefore = len(keyStringBefore)
   debugLog( "deltaSkipKeyStringBefore is " + str(deltaSkipKeyStringBefore))
   debugLog( "posi1+delta is " + str(posi1+deltaSkipKeyStringBefore))
   subString = fullPageText[posi1+deltaSkipKeyStringBefore:posi2]
   #subString = unicode(subString).encode("utf-8")
   #subString = unicode(subString)
   debugLog ( subString)
   return subString
   # remove the ,
   #floatPoint = float(pointText.replace(',',''))
   #return floatPoint
   
def getUserPointFromPage(fullPageText):
   keyStringBeforePoint = "魔力值：</font>[<a href=\"mybonus.php\">使用</a>]:"
   keyStringAfterPoint = " <font"
   pointText = getValueBetweenStrings(fullPageText, keyStringBeforePoint, keyStringAfterPoint)
   #pointText = unicode(pointText).encode("UTF-8")
   #note the point has ,
   #floatPoint = float(pointText.replace(',',''))
   return pointText



def getLastPageId(fullPageText):
   #has a lot keystring1, so we need to start from the last one
   debugLog("working on getLastPageId")
   lastPageKeyString1 = "| <a href=\"?inclbookmarked=0&amp;incldead=1&amp;spstate=0&amp;page="
   lastPageKeyString2 = "\"><b>"

   startPositoin = fullPageText.rfind(lastPageKeyString1)
   debugLog ("startPositoin is " + str(startPositoin))
   debugLog ("From startPosition text is " + fullPageText[startPositoin:])
   
   lastPageIdText = getValueBetweenStrings( fullPageText, lastPageKeyString1, lastPageKeyString2, startPositoin)
   
   return lastPageIdText


def thank_ItemID_Online(itemId):
   
   opLog("working on thank item " + str(itemId))
   if(OnLine):   
      thankData={}
      thankData['id'] = itemId
      thankValues = urllib.urlencode(thankData)
      req = urllib2.Request(ThankUrlTemplate, thankValues)
      response = urllib2.urlopen(req)
      respPage = response.read()
      # respPage is empty
 
      #the result value is not important 
      # add the newly thanked item id into the alreadyThankedList, only if it's not already in
      opLog("thank you done")
      updateAlreadyThankedDataFile(itemId)
      sleepRandom()

   
   return


def getItemListPageByPageIdOnline(pageId):
   if(OnLine!=True):
      return

   itemListPageUrl = itemListPageLinkTemplate + pageId
   opLog("loading page:" + pageId + " url : " + itemListPageUrl)

   pageResponse = urllib2.urlopen(itemListPageUrl)
   pageText = pageResponse.read()
   time.sleep(5)
   #tempFileNamefull = TempFileName+pageId+".html"
   #opLog("Saving webpage in local "+ tempFileNamefull)
   #f = open(tempFileNamefull, 'w')
   #f.write(pageText)
   #f.close();

   return pageText

def getAllItemIDFromPage(pageText):
   itemList =[]
   keyString1 = "\"  href=\"details.php?id="
   keyString2 = "&amp;hit=1\"><b>"
   startPosi=0
   while(startPosi>=0):
      startPosi = pageText.find(keyString1, startPosi+1)
      if(startPosi<0) :
         break
      itemIdText = getValueBetweenStrings(pageText, keyString1, keyString2, startPosi)
      itemList.append(itemIdText) 
      
   #### while end

   opLog("===========================================================")
   opLog("All item id in this page is :" + str(itemList))
   opLog("===========================================================")
   
   return itemList

def getItemDetailPageOnLine(itemId):
   if(OnLine):
      itemUrl = ItemDetailUrlTemplate1 + itemId + ItemDetailUrlTemplate2
      opLog("=========================================================");
      opLog("opening item detail url: "+ itemUrl)
      detailPageText = getWebPageText(itemUrl)
      if(detailPageText==None ):
         print "error loading detail page url: " + itemUrl
   else:
     #detailPageText = loadTestFile("detailPageId22.html")
     detailPageText = loadTestFile("AlreadyThanked.htm")
   
   return detailPageText


def isAlreadyThanked_checkLocalList(itemId):
   debugLog("checking local database for " + itemId)
   if(Global.AlreadyThankedItemIDList.count(itemId)==0):
       debugLog("not in local database")
       return False
   else :
       debugLog("already Thanked")
       return True

   return True

def isItemAlreadyThanked(itemId):
    if(isAlreadyThanked_checkLocalList(itemId)):
       return True
    else:
       isAlreadyThankedOnlineResult = isItemAlreadyThankedOnLine(itemId)
    
    return isAlreadyThankedOnlineResult;

def getUserPointFromUrlOnline(url):
   if(not OnLine):
      opLog("online is false, skip getting point, return")
      return
   pageText = getWebPageText(url)
   if len(pageText)>=0:
      point = getUserPointFromPage(pageText)
   else:
      opLog("Error getting webpage , empty page returned, " + url)
      point = "Error"
   return point

def isItemAlreadyThankedOnLine(itemId):
   # always assume an item is NOT thanked, so skip checking it's detail page online
   # so we can reduce web checking work load
   if(SKIPCheckingThankedOnline):
       opLog("SKIPCheckingThankedOnline = True, skip checking online, assume NOT thanked")
       return False
   #local do not have this record. check on line
   detailPageText = getItemDetailPageOnLine(itemId)
   #print detailPageText
   
   isThanked = False

   posi = detailPageText.find(ThankedKeyString)
   if(posi>=0):
      #not thanked
      isThanked = False
      Global.ToThankItemIDList.append(itemId)
   else:
      #already thanked
      isThanked = True
      updateAlreadyThankedDataFile(itemId)

   debugLog("item " + itemId + " is already thanked? : " + str(isThanked))

   #before we leave, check current user point
   point = getUserPointFromPage(detailPageText)
   opLog("user point is now: " + point)
   
   sleepRandom()
   return isThanked



def doThankOnlineItemList(itemIdlist):

   if(not OnLine):
      opLog("online is false, skip doThanks online")
      return

   opLog("================================================================")
   opLog("working on these items: "+str(itemIdlist))
   opLog("================================================================")
   
   for tempId in itemIdlist:
   
      if( Global.thankedCountInThisSession>=MaximumItemToThank): 
         #don't thank too many one time, slow it down
         opLog("reach Maximum thank item count: " + str(MaximumItemToThank))
         break
      opLog("working on item " + tempId)
      isThanked = isItemAlreadyThankedOnLine(tempId)
      
      if(isThanked==False):
         debugLog("item " + tempId + " is not thanked");
         thank_ItemID_Online(tempId)
         Global.thankedCountInThisSession += 1
         opLog("thankedCountInThisSession is "+ str(Global.thankedCountInThisSession) + ", Max item is " + str(MaximumItemToThank))

      else:
         opLog("item " + tempId + " is already thanked, skip");

   return


def doThankAllItemsOnPageId(pageId):
   opLog("working on item list page " + pageId)
   if(OnLine):
      itemListPageText = getItemListPageByPageIdOnline(pageId)
   else:
      itemListPageText = loadTestFile(TempFileName+"59"+".html" )
      #itemListPageText = loadTestFile("AllItemList.html")

   #point = getUserPointFromPage(itemListPageText)
   #opLog("======================================================")
   #opLog("   User point is now: " + point)
   #opLog("======================================================")

   #print "itemListPageText is "  + itemListPageText
   itemsFromOnePageList = getAllItemIDFromPage(itemListPageText)

   itemsFromOnePageList.sort()
   #Global.AvailabelItemIDList.extend(itemsFromOnePageList)

   toThankItemList = []
   skipItemIdList = []
   for tempId in itemsFromOnePageList:
       if (not isAlreadyThanked_checkLocalList(tempId)):
           toThankItemList.append(tempId)
       else:
           skipItemIdList.append(tempId)
   
   opLog("id found in local database, skipping these: " + str(skipItemIdList))
   doThankOnlineItemList(toThankItemList)
       
   opLog("DONE working on page id " + pageId)
   return


def main():

   loadDataAlreadyThanked()
   #return;

   opLog("working on login Page")
   if(OnLine):
      loginOK = openLoginPageOnline()
      if(not loginOK):
         opLog("login error, double check your account name and password")
         return


   opLog("working on loading mainPage")
   if(OnLine):
      textMainPage = loadMainPageOnline()
   else:
      textMainPage = loadTestFile(u"AllItemList.html")
  
   Global.oldPoint = float(getUserPointFromPage(textMainPage).replace(",",""))
   opLog("=====================================================")
   opLog("current Point is " + str(Global.oldPoint))
   opLog("=====================================================")
   lastPageId = getLastPageId(textMainPage)
   opLog("last page id is " + lastPageId )

   StartingPage = min(int(lastPageId), StartingPageSetting )


   ##################################################################
   pointThread = MyCheckUserPointThread(300)
   pointThread.start()
   

   ##################################################################
   # Start working on each page from StartingPage id
   opLog("Starting from page " + str(StartingPage))
   tempPageId = StartingPage
   Global.thankedCountInThisSession = 0
   while(True):
      
      if(tempPageId<0) :
         break
      if( Global.thankedCountInThisSession>=MaximumItemToThank): 
         opLog("reach Maximum thank item count: " + str(MaximumItemToThank))
         break   
      # loop through each page
      doThankAllItemsOnPageId(str(tempPageId))
      tempPageId = tempPageId-1

   pointThread.requestStop()

   if(OnLine):
      outPutUserPointInfo()
      
   opLog("all done")


# end

main()



