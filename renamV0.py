import threading
import time
import Queue


import os
import fnmatch


OldSubStr = " ";
NewSubStr = "";
TXTFilter = "*.txt"
WorkPath ="."

   
MAXQUEUESIZE = 20
INVALIDVALUE = -999
PRODUCER_PERIOD = 0.11
CONSUMER_PERIOD = 0.3
SHOWINFO_PERIOD = 0.5

 
 

      
def getFileList(path, filter="*.*"):

   list = os.listdir(path);
   filteredList =[]
   
   for file in list:
      if fnmatch.fnmatch(file, filter):
         filteredList.append(file)
     
   return filteredList 

   ## return newName
def getNewName(file, oldSubStr, newSubStr):

  oldName = file
  newName = oldName.replace(oldSubStr, newSubStr)
  
  return newName
  # os.rename(src, dst)

     
def doRename(filelist, oldsubstring, newsubstring):

   for file in filelist:
      
      newName = getNewName(file, oldsubstring, newsubstring);
      #
      if( not (file==newName)):
         #if old == new, nothing to change, else
         print(file + " new name is " + newName)
         os.rename(file,  newName) 

      
def doBatchRename(workpath, filter, oldSubStr, newSubStr):

   print("workpath is " + workpath)
   print ("filter is " + filter)
   print("Replace "+ oldSubStr + " with "+ newSubStr)
   #1  get all names (filter applied)
   
   #2 output rename result on screen before actual action 
   
   #3 actual operation
   
   
   ######################################################
   #1  get all names (filter applied)
   filelist = getFileList(workpath, filter);
   if( len(filelist) ==0):
      print ("file not found: " + filter)
      #abort operation since file not found, list is zero
      return;
      
      
   #print("Files:", filelist);
   ######################################################
   
   ######################################################
   #2 output rename result on screen before actual action 
   ############
   
   print ("start preview");
   
   # file exists, and new name != old name
   needRenameFileCount =0
   
   for file in filelist:
      
      newName = getNewName(file, oldSubStr, newSubStr);
      if(not newName == file):
         needRenameFileCount = needRenameFileCount +1
         print("file " + file + " , new name is: " + newName)
      
   if  needRenameFileCount == 0:
      print("No file need to rename")
      return
   
   shouldDo = raw_input("Correct and do it ? Type yes to perform actual rename action. (yes/no) ")
   print("Should take actual action ? " + shouldDo);
   
   if( shouldDo =="yes"):
      doRename(filelist, oldSubStr, newSubStr);   
   else:
      print ("action cancelled")
   
   ######################################################
   
   
   


def main():

   # TXTFilter = "*.txt"
   doBatchRename(WorkPath, TXTFilter, "-Copy","Copy");
   
    
  
   
main()
   
   
   