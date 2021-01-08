def print_time(threadName,delay):
  count =0
  while count < 5:
    time.sleep(delay)
    count +=1
    print(threadName, delay)
    
try:
  _thread.start_new_thread(print_time_func,  ("thread1", 2, ))
  _thread.start_new_thread(print_time_func,  ("thread2", 4, ))
  
