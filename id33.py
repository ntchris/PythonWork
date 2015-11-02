#from ID3 import *

# set track number from the filename
import os
import fnmatch
from  ID3 import *

WorkPath = "D:/temp/"
ID3_FieldName="TRACKNUMBER"
MP3FileNameExtention = ".mp3"
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
  
    
def getFileList(path, filter= MP3FileFilter):

   list = os.listdir(path);
   filteredList =[]
   
   for file in list:
      if fnmatch.fnmatch(file, filter):
         filteredList.append(file)
     
   return filteredList 

  
def setTrackNumByFileName(workpath, fileNameIgnorePart =""):
    
    list = getFileList(workpath)
    for file in list:
       try:
          
          newTrackNum = getTrackNum(file, fileNameIgnorePart)
          #id3info = ID3(workpath+"/"+file)
          id3info = ID3(workpath+file)
          print ("Old track # " + id3info[ID3_FieldName])
          print("setting new TrackNum is ", newTrackNum)
       
          #auto update!!
          id3info[ID3_FieldName]=newTrackNum
          
          print("now track num is set:", id3info[ID3_FieldName])
          id3info.write()
          print id3info.filename
          
          for k, v in id3info.items():
             print k + " " + v
       except ValueError: 
          # file name is not number ignore
          print ("Ignored, File name is not number: "+file)
       
    
    

def main():
   setTrackNumByFileName(WorkPath, "aa")
   

main()