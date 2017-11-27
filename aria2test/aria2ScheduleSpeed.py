# to detect what is the service port for the aria2c rpc (well, the one I didn't started)

import urllib2, json
import threading
import time
import datetime
from pprint import pprint


myAria2cPort=296951
secret='dpn'
param_secret="token:"+secret


class Constants:
  GoodHour =1
  GoodMinute=57
  EndHour=8
  EndMinute=5
  
  OneMinute=60
  resultOK='OK'
  limitedSpeed="50K"      


def listMethods():
  global myAria2cPort
  jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer', 'method':'system.listMethods'})
  c = urllib2.urlopen("http://localhost:"+str(myAria2cPort)+"/jsonrpc", jsonreq)
  pprint(json.loads(c.read()))


found=False
#{u'id': u'qwer',
# u'jsonrpc': u'2.0',
# u'result': [u'aria2.addUri',
            #u'aria2.addTorrent',
#...

def listNotifications():
  jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer', 'method':'system.listNotifications'})
  c = urllib2.urlopen('http://localhost:6800/jsonrpc', jsonreq)
  pprint(json.loads(c.read()))


def listNotifications(port):
  global found
  print("testing "+str(port))
  jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer', 'method':'system.listNotifications'})
  urlbase="http://localhost"
  urlservice="jsonrpc"
  url=urlbase+":"+str(port)+"/"+urlservice
  
  try:
    c = urllib2.urlopen(url, jsonreq)
    pprint(json.loads(c.read()))
    print("found! port is "+str(port)+"!!!")

    found=True
  except urllib2.URLError as error:
    #print error
    pass
  
  
## found, 9695
def findPort():
  global found
  for i in range (2, 65535):
  #  listNotifications(i)
     print("found is "+str(found))
     if(found):
        print ("found and break!")
        break
     threading.Thread(target=listNotifications, args=[i]).start()
     time.sleep(0.01)
  



def getCurrentGlobalOptions():
   global myAria2cPort
   global param_secret
  
   jsonreq = json.dumps(  {'jsonrpc':'2.0', 'id':'qwer','method':'aria2.getGlobalOption','params':[param_secret]} )
   #print("!requesting "+jsonreq)
   print("getting global option...")
   urlbase="http://localhost"
   urlservice="jsonrpc"
   url=urlbase+":"+str(myAria2cPort)+"/"+urlservice
   
   try:
      resp = urllib2.urlopen(url, jsonreq)
      goption=json.loads(resp.read())
      #print(goption)
      result=goption['result']
      
   except urllib2.URLError as error:
      print error
      print ("aria not running or wrong port")
      result="error can not get goption"
      pass
    
   #print("result is "+str(result))
   return result
  

   
def getGlobalSpeedLimit( ):
   goption=getCurrentGlobalOptions()
   return getGlobalSpeedLimitz(goption)
   
def getGlobalSpeedLimitz(goption):
   
   speed=goption['max-overall-download-limit']     
   return speed


def setGlobalSpeedLimit(speedLimit):
   global myAria2cPort
   global param_secret
   
   print("setting speedlimit to "+str(speedLimit))
   options = {"max-overall-download-limit":speedLimit }
   jsonreq = json.dumps(  {'jsonrpc':'2.0', 'id':'qwer','method':'aria2.changeGlobalOption','params':[param_secret , options ] } )
   #print("!requesting "+jsonreq)
   urlbase="http://localhost"
   urlservice="jsonrpc"
   url=urlbase+":"+str(myAria2cPort)+"/"+urlservice
   
   try:
      resp = urllib2.urlopen(url, jsonreq)
      respJson=json.loads(resp.read())
      result = respJson["result"]
      result=result.strip()
      
      if(result== Constants.resultOK):         
         print("OK")
         return True
      else:
         print(respJson)
         return False      

   except urllib2.URLError as error:
      print error
      return False
    
   return False
  
  

def checkForGoodTime(goodtime, endtime):

    nowTime= datetime.datetime.now()    
    print("now is " + str(nowTime))
    return (nowTime > goodtime ) and ( nowTime < endtime) 
           
    
def test():
   listMethods()
   getCurrentGlobalOptions()
   setGlobalSpeedLimit("101")   
   getCurrentGlobalOptions()
 
      
def main():
  
   nowTime= datetime.datetime.now()    
   GoodTime = nowTime.replace(hour=Constants.GoodHour, minute=Constants.GoodMinute, second=0, microsecond=0)
      
   EndTime= nowTime.replace(hour=Constants.EndHour, minute=Constants.EndMinute, second=0, microsecond=0)


   currentSpeedLimit=getGlobalSpeedLimit()
   print ("current Global speed limit is "+currentSpeedLimit)

   setSpeedLimit = False
   while True:
     if( checkForGoodTime(GoodTime, EndTime)):
       print("Good time, setting limit to 0")
       setGlobalSpeedLimit("0")
       break;
     else:
       if(not setSpeedLimit) :
         setGlobalSpeedLimit(Constants.limitedSpeed)
         setSpeedLimit=True

       print("not yet good time, sleeping")
       time.sleep(2*Constants.OneMinute)
      


main()


  