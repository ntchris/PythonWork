import threading
import time

def doWork():
   for i in range(10):
      print("doing work! " + str(i))
      time.sleep(0.6)
         
def main():
    MAX=5
    threadList = []
    for i in range(MAX):
         t = threading.Thread(target=doWork, name="thread"+str(i))
         t.daemon = False
         threadList.append(t)
         t.start()
         time.sleep(0.4)

         #t.join()
    
    # this block the main thread from running, until the threadList are all done 
    for t in threadList:
       t.join()
        
                 
    
    print("in main")
    
        
              
    print("end of main")
           
main()
 