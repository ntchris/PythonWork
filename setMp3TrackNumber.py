#from ID3 import *

# set track number from the filename
import os
import fnmatch
from  ID3 import *

WorkPath = u"F:/music/粤语评书《倚天屠龙记》全210回(001-110回)(播讲：张悦楷){听书族Www.TingShuZu.com}/"
ID3_FieldName="TRACKNUMBER"
MP3FileNameExtention = u".mp3"
MP3FileFilter = "*"+MP3FileNameExtention

def getTrackNum(file, ignorePart=""):
   
   # skip the extension first 
   file = file.replace(MP3FileNameExtention,"")
   
   if(ignorePart!=""):
       print "replacing "  + ignorePart
       file = file.replace(ignorePart, "")
       print "replaced file name is " + file
   
   trackNum = int(file)
   
   return trackNum
  

# get the first number part from the file name
def getTrackNumV2(file, ignorePart=""):
   
   if(file=="") :
      print "File name is empty ??"
      return;
      
   trackNum = 0
   file = file.replace(MP3FileNameExtention,"")
   if(ignorePart!=""):
       print "replacing "  + ignorePart
       file = file.replace(ignorePart, "")
       
   index = 0;
   maxLen = len(file)
   ifCountingStarted = False
   while index<maxLen :
      #print file[index]
      
      try: 
         currentdigit = int(file[index])
         trackNum = trackNum * 10 + currentdigit
         if(not ifCountingStarted):
            ifCountingStarted = True
      except ValueError:   
         if(ifCountingStarted): 
            ## if counting already started then it's time to end.
            break
            
      index += 1
   
    
   print "analys done, trackNum is "  + str(trackNum)
   return trackNum
  
  
def getFileList(path, filter= MP3FileFilter):

   list = os.listdir(path);
   filteredList =[]
   
   for file in list:
      if fnmatch.fnmatch(file, filter):
         filteredList.append(file)
     
   return filteredList 

  
def setTrackNumByFileName(workpath, fileNameIgnorePart =""):
    try:
        list = getFileList(workpath)
        for file in list:
           print("\n")
           print "checking file "  + file
           id3info = ID3(workpath+"/"+file)
           
           try:    
              newTrackNum = getTrackNumV2(file)          
           except ValueError: 
              # file name is not number ignore          
              print ("Ignored, File name is not number: "+file)
              continue   
              
           #print ("Old track # " + id3info[ID3_FieldName])
           if(newTrackNum<=0): 
               print "Can not find new track number, ignored"
               continue   
                 
           print("setting new TrackNum is " + str(newTrackNum))
           
           try:
              #auto update!!
              id3info[ID3_FieldName]=newTrackNum
              
              id3info.write()
              print id3info.filename
           except  :
              print ("File access error " + file)
              continue       
           
              
           #for k, v in id3info.items():
            #  print k + " " + v 
           
        print("\n")
    except :
        print("some file ignored")
   
    

def main():

   print ("If have problem setting some track number, use foobar to set empty for all the track # first")
   
   setTrackNumByFileName(WorkPath)
   print ("done")
   
  
     

main()