import threading
import time
import Queue


import os
import fnmatch


OldSubStr = u"Patch.UP0082-CUSA01633_00-FINALFANTASYXV00-A0123_keystone.Patch";
NewSubStr = u"Patch. Final.Fantasy.15.CUSA01633.US.PS4_A0123_keystone.Patch";
WorkPath =u"D:\Final.Fantasy.15.CUSA01633.US_with.Patch.123_keystone"

TXTFilter = u"*.txt"
MP3Filter =u"*.mp3"
RarFilter =u"*.rar"
#WorkPath ="."

oldNewNameMapping = dict()

   
   
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
  

     
def doRename(filelist, workpath):

   for file in filelist:
      
      try:
        newName = oldNewNameMapping[file]
        #
        if( not (file==newName)):
           #if old == new, nothing to change, else
           print(file + " new name is " + newName)
           try:
              os.rename(workpath + "/"+ file,  workpath + "/"+ newName) 
           except WindowsError as er:
              print (file + " to " + newName + " : error: " + str(er))
              continue
      except KeyError:
        #ignore because it doesn't need rename      
        continue

      
def doBatchRename(workpath, filter, oldSubStr, newSubStr):

   print("workpath is " + workpath)
   print ("filter is " + filter)
   print("Replace "+ oldSubStr + " with "+ newSubStr)
   #1  get all names (filter applied)
   
   #2 output rename result on screen before actual action 
   
   #3 actual operation
   
   if(oldSubStr==""):
      print ("nothing to replace")
      return
   
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
   
   
   for file in filelist:
      
      newName = getNewName(file, oldSubStr, newSubStr);
      if(not newName == file):
         oldNewNameMapping[file]=newName
         
         print("file " + file + " , new name is: " + newName)
      
   if  (len(oldNewNameMapping) == 0):
      print("No file need to rename")
      return
   
   shouldDo = raw_input("Correct and do it ? Type yes to perform actual rename action. (yes/no) ")
   print("Should take actual action ? " + shouldDo);
   
   if( shouldDo =="yes"):
      doRename(filelist , workpath);   
   else:
      print ("action cancelled")
   
   ######################################################
   
   
   


def main():

   # TXTFilter = "*.txt"
   doBatchRename(WorkPath, RarFilter, OldSubStr,NewSubStr);
   
    
  
   
main()
   
   
   