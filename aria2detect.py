# to detect what is the service port for the aria2c rpc (well, the one I didn't started)

import urllib2, json
import threading
import time
from pprint import pprint

def listMethods():
  jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer', 'method':'system.listMethods'})
  c = urllib2.urlopen('http://localhost:6800/jsonrpc', jsonreq)
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
  
  

  
def main():

  #listNotifications(6800)
  global found
  for i in range (2, 65535):
  #  listNotifications(i)
     print("found is "+str(found))
     if(found):
        print ("found and break!")
        break
     threading.Thread(target=listNotifications, args=[i]).start()
     time.sleep(0.01)
  
main()
