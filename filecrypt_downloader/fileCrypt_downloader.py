import urllib.request
import urllib.error 
from fake_useragent import UserAgent
import time
import json
import os
import math


from html.parser import HTMLParser
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


class FileCryptParser(HTMLParser):
    
    class FileObj:
        filename=None
        fileCryptOpenLink=None   # the openlink function generate a fileCryptLink
        fileCryptRealLink=None # the real file crypt link has id
        zippyLink=None # the zippy link 
        def toTuple(self):
            return self.filename, self.fileCryptOpenLink, self.fileCryptRealLink, self.zippyLink
        def __init__ (self, tuple=None):
            if(tuple!=None):
               self.filename, self.fileCryptOpenLink, self.fileCryptRealLink,self.zippyLink =tuple
         
        
    filelist = list()
    currentFilename = None
    currentfileCryptLink = None
    startFrom = 0
    startfromCounter=0
    cookie="" 
    
    def parseFileCryptUrlAndGetFileList(self, filecrypturl, startfrom):
        
        html_text= self.openFileCryptMainUrl(filecrypturl)
        
        self.parseFileCryptOpenLinks(html_text, startfrom)
        self.onlineParseRealFileCryptLinks()
        self.onlineGetZippyFileLinks()
        
        return self.filelist
        
        
    def parseFileCryptNewPageToGetNewLink(self, html_text):
        
        url=None
        keyword="src=\"https://filecrypt.cc/index.php?Action=Go&id="
        temp, url= html_text.split(keyword)
        url, temp=url.split("\"></iframe>")
        
        keyword = keyword.replace("src=\"","")         
        url=keyword+url
        print("realFileCrypt url is ", url )
        return url
        
    def fileCryptOpenLinkToRealFileCryptLink(self, openlink):
        realfilecryptlink=None
        
        response = self.openUrlWithCookie(openlink, self.cookie)
        newpage_text = response.read().decode('UTF-8')
        
        realfilecryptlink= self.parseFileCryptNewPageToGetNewLink(newpage_text)        
        return realfilecryptlink
    
    # return response
    def openUrlWithCookie(self, url, cookie=None):
           req = urllib.request.Request(url, data=None, headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11' })            
           if( cookie!=None or cookie!=""):
               req.add_header('cookie',  cookie)
        
           response = urllib.request.urlopen(req  )
           return response
                 
    def onlineParseRealFileCryptLinks(self):
        # cookie jhjn7ml3mtdpdgs2tmavoa6vt2
        # PHPSESSID
        newlist=list()
        i=0
        for tuple in self.filelist:           
           
           i=i+1
           fileObj = self.FileObj(tuple)
           fileObj.fileCryptRealLink= self.fileCryptOpenLinkToRealFileCryptLink(fileObj.fileCryptOpenLink)
           newlist.append(fileObj.toTuple())
           time.sleep(3)
        
        self.filelist= newlist
        outfile = open( "output.json", "w")
        json.dump(self.filelist, outfile)
        
        return             
    
    def openFileCryptMainUrl(self, url):
        
        # cannot use this , we need the cookie
        # html_text = self.openUrlWithCookie(url)
        
        req = urllib.request.Request(url, data=None, headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11' })            
            
        response = urllib.request.urlopen(req  )
        self.cookie = response.headers.get('Set-Cookie')
        print("cookie is ",  self.cookie)
        html_text = response.read()
        f = open("fileCryptPage.html", "w")
        f.write(str(html_text))
        f.close()        

        return html_text.decode("UTF-8")

    def onlineGetZippyFileLinks(self):
        newlist=list()
        for tuple in self.filelist:
            fileObj= self.FileObj(tuple)
            response = self.openUrlWithCookie(fileObj.fileCryptRealLink, self.cookie )
            fileObj.zippyLink = response.geturl()
            newlist.append(fileObj.toTuple())
            print("zippylink is ", fileObj.zippyLink )
            time.sleep(2)
        
        self.filelist = newlist
      
        return
      
      

    # pattern: file name pattern, .rar or .zip etc
    def parseFileCryptOpenLinks(self, html_text, startfrom):
        
        self.startfrom = startfrom
        # everything is inside tbody tag
        tbodyText = self.extra_tbody_text_from_html(html_text)
        
        self.feed(tbodyText)            
               
        return  
    
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

    def getFileCryptLinkFromOpenLink(self, openlink):
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
              if( self.startfromCounter < self.startfrom):
                 self.startfromCounter=self.startfromCounter+1
                 self.currentFilename = None 
                 
               
              self.currentFilename = fname
                            
                
        elif (tag == Constants.Tag_button):
           # no file name, ignore link
           if(self.currentFilename == None):
               return
           
           openlink = self.getButtonLink(attrs)
           
           self.currentfileCryptLink = self.getFileCryptLinkFromOpenLink(openlink)
           
           fileobj= FileCryptParser.FileObj()
           fileobj.filename= self.currentFilename 
           fileobj.fileCryptOpenLink  = self.currentfileCryptLink
           
           self.filelist.append(fileobj.toTuple())

    def handle_endtag(self, tag):    
        return     

    def handle_data(self, data):        
        return 
    

class ZippyShareDownloader():
    
    def getZippyPage(self, filename, zippylink):
        
        req = urllib.request.Request(zippylink, data=None, headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11' })            
            
        response = urllib.request.urlopen(req  )
        #self.cookie = response.headers.get('Set-Cookie')
        #print("cookie is ",  self.cookie)
        html_text = response.read()
        zf=open(filename+"_zippy.html","wb")
        # html_text= html_text.decode('UTF-8')
        zf.write( html_text )
        zf.close()        

        return html_text.decode('UTF-8')
        
    def getVarAandB(self, script_part):
        a , bpart = script_part.split(";",1)
        #print(a)
        
        temp, b= bpart.split("b = ")
        b, temep = b.split(";",1)
            
        
        #print(b)    
        return int(a),int(b)
    
        
    def parseZipyyPage(self, url, zippyHtml):
        ##
        ## https://www112.zippyshare.com/d/Vu1g86TI/948272/EP1003-CUSA00375_00-EVILWITHINDLC001-A0000-V0100.part07.rar
        ## https://www112.zippyshare.com/d/Vu1g86TI/"+(a + 727691%b)+"/EP1003-CUSA00375_00-EVILWITHINDLC001-A0000-V0100.part07.rar

        script_keyword1= "<script type=\"text/javascript\">\n    var a = "
        script_keyword2= "</script>"
        temp, script_part = zippyHtml.split(script_keyword1)
        script_part, temp = script_part.split(script_keyword2,1) 

        #print("script_part", script_part)
        
        a, b= self.getVarAandB(script_part)
        
        newa = math.floor( a/3 ) 
        
        equation = newa + a % b
        keyword="document.getElementById('dlbutton').href = \""
        temp, realurl= script_part.split(keyword)
        realurl, temp= realurl.split("\";",1)
        # print(realurl)
        
        part1, part2 = realurl.split("\"",1)
        temp, part2 = part2.split("\"")
        
        realurl=part1+ str(equation) +part2
        
        o= urllib.parse.urlparse(url)
        fullurl= o.scheme+"://" + o.netloc+ realurl
        print("full url", fullurl)
        return fullurl
        
    def downloadFile(self, filename, zippylink):
        print("downloading " + filename + " "+ zippylink)        
        
        zippyHtml = self.getZippyPage(filename, zippylink)
        reallink = self.parseZipyyPage(zippylink, zippyHtml)
        
        # save, write the file 
        urllib.request.urlretrieve(reallink, filename)  
        
        return

    def downloadFileList(self, fileList):
        
        for tuple in fileList:
           filename, temp, temp2, zippylink= tuple 
           self.downloadFile(filename, zippylink)
           time.sleep(1)
           
        #for fileObj in fileObjList :
        #   self.downloadFile(fileObj.zippyLink)
            
        #self.downloadFile(fileObjList[0].zippyLink)
        return 
#   
   
def printList(filelist):
    
    for tuple in filelist:
       fileObj= FileCryptParser.FileObj(tuple)
       print(fileObj.filename,  fileObj.fileCryptOpenLink, fileObj.fileCryptRealLink, fileObj.zippyLink )
         
        
          
#def parse_fileCrypt_html_to_real_link(html_text , pattern):
 
#    parser = FileCryptParser()      
               
#    return parser.getFileLinks(html_text, pattern)

def parse_fileCrypt_url_to_zippy_link(filecryptUrl, startfrom):
        
    parser = FileCryptParser()
    
    return parser.parseFileCryptUrlAndGetFileList(filecryptUrl, startfrom)
 

def main():
    
    fileCryptUrl ="https://filecrypt.cc/Container/F9E561FD4E.html"
    
    #f = open("Filecrypt2.html", "rt")
    #html_text = f.read()
    
      
    
    # reallinks is a list of filename and link pair
     
    fileObjList= parse_fileCrypt_url_to_zippy_link(fileCryptUrl, 178)
    
    outfile = open( "outputzippy.json", "w")
    json.dump(fileObjList, outfile)
        
    printList(fileObjList)
    
    zippy = ZippyShareDownloader()
    
    filelist=list()
    jsonfileObj = open("outputzippy.json", "r")
    filelist = json.load(jsonfileObj)
    
    #zippy.downloadFileList(filelist) 

    print("done!")
main()
