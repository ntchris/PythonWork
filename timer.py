import time
import sys

class Constant:
    HOUR = 2
    MIN = 0



def waitForNSecondsOrPressKey(waitTime, key):
   for sec in range(0, waitTime):
      print("waiting " + str(sec))
      char  = sys.stdin.read(1)
      print("Press " + key + " in " + str(waitTime) + " seconds")
      time.sleep(1)
   
   print("Received input is : " + str( string))




def isGoodDownloadTime():
    
   isgood = False
   timestruct = time.localtime()
      
   print timestruct
   print timestruct.tm_hour
   print timestruct.tm_min

   if (timestruct.tm_hour<Constant.HOUR and timestruct.tm_min<=Constant.MIN):
      print 'good time'
   else:
      print 'no good time'
   return False


def main():

  

  print "isGoodDownloadTime " + str(isGoodDownloadTime())
  #print "isGoodDownloadTime " + str(isGoodDownloadTime)

  return 0
  WAITTIME = 5;
  waitForNSecondsOrPressKey(WAITTIME, "Q")

  print ("continue...")
  
#if __name__ == "__main__":



main()



