Allow = ["!","\"","/", "\\","[","]" , ":", "{","}","<",">", ",","'", "-", ">","<","."," ","\r","\n","?","&","(",")"]
minChineseChar = 0x3610
import glob
import sys
import urllib
import urllib2
import cookielib
import time
import random
import os
import threading
import codecs

def isEngNumOnly(str):
    
   if(char.isalpha() or char.isdigit()  or char in Allow):       
      return True
   else:
      #print char 
      return False
         
   return True

def isChinese(char):
   
   #print hex(ord(char))
   if( ord(char) >= minChineseChar):
      #print "is , remove"   
      return True
   else:
      return False
      
def removeChinese(inString):
   
   #utf8 files:  
   #inString = inString.decode("utf-8")
   
   #inString = inString.decode("utf-8", 'ignore')
   
   #inString = unicode(inString)
   
   #inString = inString.encode("utf-8") xxxx
   
   #inString = inString.encode("ascii") #UnicodeDecodeError: 'ascii' codec can't decode byte 0xb1 in position 1: ordinal not in range(128)
   
   #inString = inString.decode("ascii") #UnicodeDecodeError: 'ascii' codec can't decode byte 0xb1 in position 1: ordinal not in range(128)
   
   #inString = unicode(inString)
   #inString = inString.decode("utf-8")
   #inString = inString.encode("utf-8")
   
   #inString = unicode(inString, "ascii")
   #if(type(inString)==str):
   #   print "!!! str"
   #   unicodestr = unicode(inString, "ascii")
   #   return
   #else:
   #   inString = inString.decode("utf-8")
      
   #print "the type is " + str(type(inString))
   
   
   
   #print inString
   tempList = list(inString)
   
   for index, char in enumerate(tempList):
      if( isChinese(char)): 
         #print "replaced Char is " + char
         tempList[index] = ""
   outString="".join(tempList)
   #!!!
   return outString



def removeChsFile(infile):
   infileName, infileExt = os.path.splitext(infile)
   newfilename = infileName + ".eng" + infileExt
   origfile = codecs.open(infile, "r", "utf8")
   
   try:
      intext = origfile.read() 
   except:
      
      print "only support UTF-8 format files"     
      print "trying asc mode"
      origfile = codecs.open(infile, "r")
      intext = origfile.read() 
      intext = unicode(intext, "gb2312" , errors='ignore')
      #intext = unicode(intext, "gb2312")
      #print intext
   
   newFile = open(newfilename, "w");
   
   newText = removeChinese(intext)
   #if isUTF:
   newText = newText.encode('utf-8')   

   newFile.write(newText);
   origfile.close()
   newFile.close()
   print "output file " + newFile.name + " is done"
   return 

   
   
def doFile(infile):

   infileName, infileExt = os.path.splitext(infile)
   newfilename = infileName + ".eng" + infileExt
    
   
      #origfile = open(infile, 'rU')
   origfile = codecs.open(infile, "r", "utf8")
   #print origfile.read() 
   
   
   newFile = open(newfilename, "w");

   
   try:
      for line in origfile:
         newline = removeChinese(line)
         if(newline!=""):
             newFile.writelines(newline);
   except:
      print "only support UTF-8 format files"
      return
      
   origfile.close()
   newFile.close()
   print "output file " + newFile.name + " is done"
   return 

def getFileList(fname):
    for file in glob.glob(fname):
       print(file)
     
   
  
def main():
   if len(sys.argv)<=1:
      print "usage:  subRemoveChs.py  yourFile.srt or *.ass"
      return

   subfiles = sys.argv[1]
   #removeChsFile(subfile)
   
   filelist = glob.glob(subfiles)
   
   if( len(filelist)<=0):
      print "wrong file name"
      return
      
   for file in filelist:
      print("working on " + file)
      removeChsFile(file)
     
     
    
   
   return   
   
   
main()
