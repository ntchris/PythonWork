# to detect what is the service port for the aria2c rpc (well, the one I didn't started)

import urllib2, json
import threading
import time
import datetime
from pprint import pprint

myAria2cPort=9695
secret='abcdmadpanz'
param_secret="token:"+secret


class Constants:
    GoodHour =1
    GoodMinute=57
    


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
   print("!requesting "+jsonreq)
   urlbase="http://localhost"
   urlservice="jsonrpc"
   url=urlbase+":"+str(myAria2cPort)+"/"+urlservice
   
   try:
      resp = urllib2.urlopen(url, jsonreq)
      goption=json.loads(resp.read())
      print(goption)
      result=goption['result']
      print(result['max-overall-download-limit'])
      
   except urllib2.URLError as error:
      print error
      pass
    
   return
  

def setGlobalSpeedLimit(speedLimit):
   global myAria2cPort
   global param_secret
   
   options = {"max-overall-download-limit":speedLimit }
   jsonreq = json.dumps(  {'jsonrpc':'2.0', 'id':'qwer','method':'aria2.changeGlobalOption','params':[param_secret , options ] } )
   print("!requesting "+jsonreq)
   urlbase="http://localhost"
   urlservice="jsonrpc"
   url=urlbase+":"+str(myAria2cPort)+"/"+urlservice
   
   try:
      resp = urllib2.urlopen(url, jsonreq)
      print(json.loads(resp.read()))
   except urllib2.URLError as error:
      print error
      pass
    
   return
  
  

def checkForGoodTime():
    nowTime = time.localtime()
    
    nowTime= datetime.datetime.now()    
    today2AM = nowTime.replace(hour=Constants.GoodHour, minute=Constants.GoodMinute, second=0, microsecond=0)
    
    if (nowTime  < today2AM):
        print ("small, " + str(nowTime) )
        
    else :
        print ("later, "+ str(nowTime ))
        print ("difference: is " + str(nowTime-today2AM))
    
    
def test():
   listMethods()
   getCurrentGlobalOptions()
   setGlobalSpeedLimit("101")   
   getCurrentGlobalOptions()
 
      
def main():
   
   ###test()
   checkForGoodTime()


main()


  