import time
import sys

def waitForNSecondsOrPressKey(waitTime, key):
   for sec in range(0, waitTime):
      print("waiting " + str(sec))
      char  = sys.stdin.read(1)
      print("Press " + key + " in " + str(waitTime) + " seconds")
      time.sleep(1)
   
   print("Received input is : " + str( string))


def main():

  WAITTIME = 5;
  waitForNSecondsOrPressKey(WAITTIME, "Q")

  print ("continue...")
  
#if __name__ == "__main__":
main()

