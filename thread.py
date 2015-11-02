import threading
import time
import Queue
 
MAXQUEUESIZE = 20
INVALIDVALUE = -999
PRODUCER_PERIOD = 0.11
CONSUMER_PERIOD = 0.3
SHOWINFO_PERIOD = 0.5


class MyQueue():
   
   def __init__( self, maxSize = MAXQUEUESIZE ):
       
      self._queue = Queue.Queue(maxSize)
      self.isBusy = False
   
   def __del__(self):
      print ("Deleting MyQueue")
      

      
   def addItem(self, newItem):       
      self._queue.put(newItem)   
       
       
       
   def getItem(self):          
       item = self._queue.get()       
       return item
     
   def isEmpty(self):
      return self._queue.empty()
      
   def printInfo(self):
      
      self.isBusy = True
      print("current Size:" + str(self._queue.qsize()))      
      print(self._queue.queue)
      self.isBusy = False

   def taskDone(self):
      self._queue.task_done()

   def join(self):
      self._queue.join()

      
class MyProducerThread(threading.Thread):
   def __init__(self, workQueue, name):
      threading.Thread.__init__(self)
      self.toStop = False
      self.workQueue = workQueue
      self.name = name
      print ("thread " + self.name + " initing")
   
      self.currentItem = 0
      self.setDaemon(True)
      
   def run(self):
      self.toStop = False
      print("Producer " + self.name + " Thread running")
      while(not self.toStop):        
      
        if(not self.workQueue.isBusy) :
           self.currentItem = self.currentItem+1
           print("producing and adding " + str(self.currentItem));
           self.workQueue.addItem(self.currentItem)
           
           
        else :
           print("Producer: Queue is Busy !" +  (time.asctime()))
   
        print("producer sleeping")
        
        if( self.toStop == True):
           return
        time.sleep(PRODUCER_PERIOD)
        print("producer waking up")        
      print("producer to stop !")  
           
   def requestStop(self):
      self.toStop = True
      

class MyConsumerThread(threading.Thread):
   def __init__(self, workQueue, name):
      threading.Thread.__init__(self)
      self.toStop = False
      self.workQueue = workQueue
      self.name = name
      print ("thread " + self.name + " initing")
   
      
      self.setDaemon(True)
      
   def run(self):
      self.toStop = False
      print("CCC " + self.name + " Thread running")
      while(not self.toStop):        
            
        if(not self.workQueue.isBusy) :
            
           item = self.workQueue.getItem()
           print("CCC and getting " + str(item));
           
        else :
           print("CCC: Queue is Busy !" +  (time.asctime()))
   
        print("CCC sleeping")
        
        if( self.toStop == True):
           return
        time.sleep(CONSUMER_PERIOD)
        print("CCC waking up")        
      
        
        
   def requestStop(self):
      self.toStop = True
      

      
      
def main():
   print ("in main() ")
   
   workQueue = MyQueue()
   
   producer = MyProducerThread(workQueue, "Producer")
   producer.start()
   
   consumer = MyConsumerThread(workQueue, "Consumer")
   consumer.start()
   
   for i in range(0, 10):
     
      workQueue.printInfo()
      time.sleep(SHOWINFO_PERIOD)
   
   
   # a few seconds passed, now request all threads to stop
   print ("requesting stop")
   consumer.requestStop()   
   producer.requestStop()
   
   
   print("end")
   
   
   
   del producer
   del consumer
   workQueue.printInfo() 
   
   del workQueue
   
   
   
     
   
main()
   