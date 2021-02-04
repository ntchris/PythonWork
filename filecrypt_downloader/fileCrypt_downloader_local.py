
import requests
 
from fake_useragent import UserAgent
import time
import json
import os
import math
import sys
from http.cookies import SimpleCookie
import pickle
from html.parser import HTMLParser

import http.cookiejar
from _ast import Try

#from tkinter.constants import CURRENT
#from fileinput import filename
#from builtins import None
#from distutils import filelist


class Constants():
    Tag_TableStart = "<table>"
    Tag_TableEnd = "</table>"
    Tag_td = "td"
    Tag_button = "button"
    Title = "title"
    OnClick = "onclick"
 
  
      
#   
   
def printList(filelist):
    
    for fileObj in filelist:       
       print(fileObj.filename,  fileObj.fileCryptOpenLink )
         
         

# ==========================================================


class FileCryptParser(HTMLParser):
    
   class FileObj:
      
      def __init__ (self, filename, openlink ):         
           self.filename = filename
           
           # the download button,  the link when you click on download button. must be open with cookies.
           self.fileCryptOpenLink = openlink
           
           # open the openlink (download button) (must using cookie), will generate a real link to the file download site
           self.fileCryptRealLink=None # the real file crypt link has id
            
            # the link in file download site, the real real real link
           self.downloadLink = None

   filelist = list()
   currentFilename = None
   currentfileCryptLink = None   
   cookie="" 

    # pattern: file name pattern, .rar or .zip etc
   def parseFileCryptOpenLinks(self, html_text  ):
        
      
      # everything is inside tbody tag
      #try:
      tbodyText = self.extra_tbody_text_from_html(html_text)
      # this will parsethe html page and create a self.filelist and fill it with filename and fake link (step 1 link)  
      self.feed(tbodyText)
        # except ValueError:         
      return  
    
   # after open the link (click download button), a new page is return
   # there is a link like this "https://filecrypt.cc/index.php?Action=Go&id=" is  in this page, grab it.
   def parseFileCryptNewPageToGetRealink(self, html_text):
       #print("html_text is")
       #print(html_text)
       url=None
       keyword="https://filecrypt.cc/index.php?Action=Go&id="
       temp, part2= html_text.split("id=")
       id = None
       try:
         id,temp = part2.split("';</script>")
       except ValueError:
         id=None
         
       if id==None:
         try:
           id, temp = part2.split("\">")
         except ValueError:
           id=None
           
           
       if( id !=None):  
          url=keyword+id
          print("realFileCrypt url is ", url )
       else:
          print("cannot parse:")
          print(html_text)
          url=None
              
       return url
        
        
   def openUrlWithCookieWithRequest(self, url   ):

       headers = {'User-Agent': 'Mozilla/5.0'}
       response =  requests.get(url, cookies= self.cookie, headers=headers)
        
       print("response is")
       print(response)
       return response
           
   def fileCryptOpenLinkToRealFileCryptLink(self, openlink):
       realfilecryptlink=None
       print( "fileCryptOpenLinkToRealFileCryptLink "  + openlink) 
       response = self.openUrlWithCookieWithRequest(openlink  )
       
       # this is still the old link
       #print(response.url)
       newpage_text = response.text
       #print( response.text)
       realfilecryptlink= self.parseFileCryptNewPageToGetRealink(newpage_text)

       return realfilecryptlink


   def onlineGetFileDownloadSiteLinks(self):
        print("onlineGetFileDownloadSiteLinks")
        for fileObj in self.filelist:
            print("opening " + fileObj.fileCryptRealLink)
            try:
                response = self.openUrlWithCookieWithRequest(fileObj.fileCryptRealLink   )
                print(response.content)                
                fileObj.downloadLink = response.url
                print("file download site link is ", fileObj.downloadLink )
            except Exception  as e :
                    fileObj.downloadLink = "" 
                    print("error!" )
                    print(e)
                    continue
            time.sleep(10)
                
        return
    
   def isValidFile(self, filename):
       if ( not ("." in filename)) :
           return False 
       
       name , ext = filename.split(".",1)
       name = name.strip()
       if len(name)==0:
           return False
          
       return True      
       
    
   # using cookie to open the download button link, call it "CryptRealLink     
   def onlineParseRealFileCryptLinks(self):
   
        i=0
        for fileObj in self.filelist:           
           i=i+1
           # only process if filename is valid, ie "n/a" is not a valid filename. no need to process further
           if self.isValidFile(fileObj.filename):
              fileObj.fileCryptRealLink= self.fileCryptOpenLinkToRealFileCryptLink(fileObj.fileCryptOpenLink)
           else:
              fileObj.fileCryptRealLink = ""
              continue
           time.sleep(10)
        
        return  
 
      
           
   def parseFileCrypHtmlFileAndGetFileList(self, htmlfile  ):
      f = open(htmlfile, "rt")
      html_text = f.read()
      # this will create a file object list with download button link, call it openlink because there is a open() function to open it in the html page
      # ie   
     # <td><button onclick="openLink('WFiBUFfxGZsGKbqOtUIiZ_VvzQAS-VxtlTnqH-l_FR6Ord05QIsQxYQ_UqDQQ2FZRQC4l772_1VD54CaF1ebXV_162hjzGZFWBTRtEC8qjl__J5M0jCastUd4WP6YYz2', this);" class="download"
      self.parseFileCryptOpenLinks(html_text )
      
      # this will use cookie to to open the above link, then to create a real lin with fileCrypt id like this
      #  <body><script type="text/javascript">top.location.href='https://filecrypt.cc/index.php?Action=Go&id=21bb3a73ddb3b3798db63435386cad242f54a63e';</script></body></html>  
        
      for fileObj in self.filelist:           
          # only process if filename is valid, ie "n/a" is not a valid filename. no need to process further
          if self.isValidFile(fileObj.filename):
             fileObj.fileCryptRealLink= self.fileCryptOpenLinkToRealFileCryptLink(fileObj.fileCryptOpenLink)
             print("opening real fileCrypt Real link with id: \n   " + fileObj.fileCryptRealLink)
             try:
                response = self.openUrlWithCookieWithRequest(fileObj.fileCryptRealLink   )
                print(response.content)                
                fileObj.downloadLink = response.url
                print("file download site link is ", fileObj.downloadLink )
             except Exception  as e :
                    fileObj.downloadLink = "" 
                    print("error!" )
                    print(e)
                    continue
     
     
          else:
             # invalid filename. 
             fileObj.fileCryptRealLink = ""
             fileObj.downloadLink = ""
             continue
          
          time.sleep(10)
        
          
                     
      self.onlineParseRealFileCryptLinks()
      
      # testing, remove the whole list, leave only one
     
     # f1=self.filelist[0]     
     # f1.fileCryptRealLink = "https://filecrypt.cc/index.php?Action=Go&id=07f5c22c8fd5c957a5484651f785b55f3aae16fe"
     
      #f2=self.filelist[1]     
      #f2.fileCryptRealLink = "https://filecrypt.cc/index.php?Action=Go&id=f2578b1ba2a8a49dc347aaa7860189a7ef13b1d6"
     
      #self.filelist= list()
      #self.filelist.append(f1)
      #self.filelist.append(f2)
     
      
      
      # this will using cookie to open the file id link to generate a real file download site link
      #self.onlineGetFileDownloadSiteLinks()
             
      return self.filelist
    
    
   def extra_tbody_text_from_html(self, html_text):
      before, table_text = html_text.split(Constants.Tag_TableStart)
      table_text, after =  table_text.split(Constants.Tag_TableEnd)
      return table_text
    
   def getAttrValue(self, attrs, attname):
        for temp_att in attrs:
            if (temp_att[0] == attname):                
                return temp_att[1]

        return None

   def isAttPresent(self, attrs, attname):
       i = 0
       for temp_att in attrs:
           if (temp_att[0] == attname):
               return i
                            
       return -1       

   def getFileCryptLinkFromDownloadButtonOpenLink(self, openlink):
        href = "http://filecrypt.cc"
        temp, real_link = openlink.split("openLink(\'")
        real_link, temp = real_link.split("\',")
        real_link = href + "/Link/" + real_link + ".html"
        # if(typeof(openLink) == 'undefined') 
        # {var openLink=function(r){location.href=_DOMAIN.replace('https','http')+'/Link/'+r+'.html';}}
        return real_link
             
   def getButtonLink(self, attrs):
       link = self.getAttrValue(attrs, Constants.OnClick)
       return link
                
   def getDownloadFileName(self, attrs):
        
       if(len(attrs) <= 0):
            return None
       index = self.isAttPresent(attrs, Constants.Title) 
        
       if(index >= 0):
          return attrs[index][1]
       return None
        
   def handle_starttag(self, tag, attrs):        
           
        if (tag == Constants.Tag_td):

           fname = self.getDownloadFileName(attrs)
           if(fname != None):               
              self.currentFilename = fname
                            
                
        elif (tag == Constants.Tag_button):
           # no file name, ignore link
           if(self.currentFilename == None):
               return
           
           openlink = self.getButtonLink(attrs)
           
           self.currentfileCryptLink = self.getFileCryptLinkFromDownloadButtonOpenLink(openlink)
           
           fileobj= FileCryptParser.FileObj( self.currentFilename ,  self.currentfileCryptLink )
           
           self.filelist.append(fileobj)

   def handle_endtag(self, tag):    
       return     

   def handle_data(self, data):        
       return 
    
    
   def getFileListFromAllDownloadButton(self , table_text):
      filelist=[]
      return filelist 
 
def extra_tbody_text_from_html(  html_text):
        before, table_text = html_text.split(Constants.Tag_TableStart)
        table_text, after =  table_text.split(Constants.Tag_TableEnd)
        
        return table_text
    
    

def parse_fileCrypt_html_file_to_real_link_list_text(htmlfile,  cookiejr):
    #f = open(htmlfile, "rt")
    #html_text = f.read()
    #table_text = extra_tbody_text_from_html(html_text )
    #print(table_text )
    
    parser = FileCryptParser()
    parser.cookie = cookiejr
    filelist = parser.parseFileCrypHtmlFileAndGetFileList(htmlfile  )    
    linktext = filelistToLinkListText(filelist )
    return linktext 

def filelistToLinkListText(filelist):
    #linklist = []
    linkListText= ""
    
    for fileObj in filelist:
       linkListText = linkListText + fileObj.filename   + "\n  "  + fileObj.fileCryptRealLink  +"\n"
    
    linkListText+="===================================\n\n"
    
    for fileObj in filelist:
       
       linkListText = linkListText + fileObj.filename   + "\n  "  + fileObj.downloadLink +"\n"
    
    return linkListText  	

def main():
   argSize = len(sys.argv)
   
   selfname= os.path.basename(sys.argv[0])
   if(argSize <=1):
      print("usage: "+ selfname + " Filecrypt.html  ( local file) ")
      # return 1

   fileCrypHtmlFile=sys.argv[1] 
 	
    #fileCrypHtmlFile = "Filecrypt_Jak3.html"
 
     
  # use firefox addon  "cookies.txt " to get the text cookie. json won't work
   cj=http.cookiejar.MozillaCookieJar ("cookies.txt")
   cj.load()

   linktext = parse_fileCrypt_html_file_to_real_link_list_text( fileCrypHtmlFile ,  cj)    
	
   outfile = open( "realink.txt", "w") 
   outfile .write(linktext)
   
   outfile.close()
   print(linktext)
     
   
   print("done!")

main()
