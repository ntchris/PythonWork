ToEmail = "chjiang@blackberry.com"
SMTPServer = 'mail.rim.net'
DataFile = "products.json"

CheckInterval = 60*90

class Global:
   WebLinkKeyName = "weblink"
   OrigPriceKeyStringBeforeKeyName = "origPriceKeyStringBefore"
   OrigPriceKeyStringAfterKeyName = "origPriceKeyStringAfter"
   SalePriceKeyStringBeforeKeyName = "salePriceKeyStringBefore"
   SalePriceKeyStringAfterKeyName = "salePriceKeyStringAfter"
 

Debug = False
OnLine = True
# always assume an item is NOT thanked already online, do not check the detail page.

OneMinute = 60
HalfHour = 30 * OneMinute
OneHour = 60 * OneMinute



###############################################################################
import urllib
import urllib2
import cookielib
import time
import os
import threading
import smtplib
import datetime
from email.mime.text import MIMEText
import json
import copy



class Product:
   DellKeyDiscountString1 = "Instant Savings"
   DellKeyDiscountString2 = "You Save"
   link = "not inited"
   origPriceKeyStringBefore = "not inited"
   origPriceKeyStringAfter = "not inited"
   salePriceKeyStringBefore = "not inited"
   salePriceKeyStringAfter = "not inited"
   lowestPrice = 0
   name = "not inited"
   origPrice = 0
   saving = 0
   salePrice = 0
   

   def __init__(self, prodname, prodlink, origpricekeystrbefore, origpricekeystrafter, saleprickeystrbefore, salepricekeystrafter ):
      self.name = prodname
      self.link = prodlink
      self.origPriceKeyStringBefore = origpricekeystrbefore
      self.origPriceKeyStringAfter = origpricekeystrafter
      self.salePriceKeyStringBefore = saleprickeystrbefore
      self.salePriceKeyStringAfter = salepricekeystrafter

   def getDiscountInfoShort(self):
      
      infoString = "New low price for " + self.name + " orig price: " + str(self.origPrice) + ", save: " + str(self.saving) + ", sale price: "+ str(self.salePrice) + " , lowest price is " + str(self.lowestPrice)
      return infoString
      
   def getDiscountInfoDetail(self):
      infoString = ""
      if self.salePrice !=0 :
         infoString = "!!!!!!!  Has discount  !!!!!!\n"
      else:
         print "No discount!"
      infoString = str(datetime.datetime.now())+ " , " + infoString + self.getDiscountInfoShort() + "\n" + self.link
      return infoString
      



class PriceChecker:
    productList = []
    
    def sendEmail(self, toEmail, msg):
       #if(not OnLine):
       return;
       s = smtplib.SMTP(SMTPServer)
       s.sendmail(toEmail, toEmail ,  msg.as_string() )
       s.quit()

    def compileEmail(self, subject, emailText):

       msg = MIMEText(emailText)
       msg['Subject'] = subject
       msg['From'] = "checker"
       msg['To'] = "ToToTo"

       return msg
 

    def addProductToList(self, product):
       self.productList.append(product)

    def setProductList(self, prodList):
        self.productList = prodList

    def priceNotificatoinHandler(self, newProductInfo, currentProductInfo):
      
             
         #print "newProductInfo " + str(newProductInfo.salePrice)
         #print "currentProductInfo" + str(currentProductInfo.salePrice)
         if(newProductInfo.salePrice != currentProductInfo.salePrice):
           
            print "price changed!!"

         if(newProductInfo.lowestPrice==0 and newProductInfo.salePrice==0):
              newProductInfo.lowestPrice = newProductInfo.origPrice
              print "here1"
         elif (newProductInfo.lowestPrice==0):
              newProductInfo.lowestPrice = newProductInfo.salePrice
              print "here2"
         if(newProductInfo.salePrice < newProductInfo.lowestPrice and newProductInfo.salePrice!=0):
            newProductInfo.lowestPrice = newProductInfo.salePrice
            subject = newProductInfo.getDiscountInfoShort()
            msgText = newProductInfo.getDiscountInfoDetail()
            msg = self.compileEmail(subject, msgText)
            self.sendEmail(ToEmail, msg)

         print "==============================================================="
         print "product name: " + newProductInfo.name
         print newProductInfo.getDiscountInfoDetail()
         print "==============================================================="
         print ""


    def keepChecking(self, sleep_sec):
       while(True):
          i = 0
          for loop_product in self.productList:
             loop_product=self.productList[i]
             
             temp_Product = copy.deepcopy(loop_product)
             #print "1 loop_product sale price is " + str(loop_product.salePrice)

             self.getProductPrice(temp_Product)

             #print "2 temp_Product sale price is " + str(temp_Product.salePrice)
             #print "3 loop_product sale price is " + str(loop_product.salePrice)

             self.priceNotificatoinHandler(temp_Product, loop_product)
            

             self.productList[i] = copy.deepcopy(temp_Product)
             #print "loop_product sale price is " + str(loop_product.salePrice)
             time.sleep(5)
             i+=1 
          print "wait for " + str(sleep_sec)+" sec"       
          time.sleep(sleep_sec)
       return    

    def hasDiscount(self, pageText, keyString):
       posi1 = pageText.find(keyString)
       if posi1 >=0:
           return True
    
    def getProductPrice(self, tmp_product):

       #print "Product name is " + product.name
       productPageText = self.getProductPage(tmp_product)

       productPageText = (productPageText).decode("utf8")

       origPrice = self.getProductPriceFromPageText(productPageText, tmp_product.origPriceKeyStringBefore, tmp_product.origPriceKeyStringAfter)
       tmp_product.origPrice = origPrice
       if(tmp_product.lowestPrice<=0):
              #print "setting lowest price" + str(product.origPrice)
              tmp_product.lowestPrice = tmp_product.origPrice

       has1 = self.hasDiscount(productPageText, tmp_product.DellKeyDiscountString1)
       has2 = self.hasDiscount(productPageText, tmp_product.DellKeyDiscountString2)

       if (not has1) and (not has2):
           tmp_product.salePrice = 0
           tmp_product.saving = 0
       else :
           tmp_product.salePrice = self.getProductPriceFromPageText(productPageText, tmp_product.salePriceKeyStringBefore, tmp_product.salePriceKeyStringAfter)
           tmp_product.saving = (tmp_product.origPrice - tmp_product.salePrice)

       return

    def getProductPriceFromPageText(self, pageText, keystringBefore, keystringAfter):
       priceText = self.getValueBetweenStrings(pageText, keystringBefore, keystringAfter)       
       if( priceText ==""):
           print "Can not find price" + " . Before:" + keystringBefore + " .After: " + keystringAfter
           return 0
       priceText = priceText.replace("$","")
       priceText = priceText.replace(",","")
       return float(priceText)

    def getProductPage(self, product):
       link = product.link
      
       if OnLine:
          pageResponse = urllib2.urlopen(link)
          pageText = pageResponse.read()
            
            
          #f = open(tempFileNamefull, 'w')
          #f.write(pageText)
          #f.close();
       else:
          f = open(product.name+".html", 'r')
          pageText = f.read()
          f.close();
     
       if( len(pageText)<=0 ):
          print "error getting page text"

       return pageText
  


    def getValueBetweenStrings(self, fullPageText, keyStringBefore, keyStringAfter, startingPoint=0):

       posi1 = fullPageText.find(keyStringBefore, startingPoint)
       debugLog("posi1 is " + str(posi1 ) + " keyStringBefore is : " + keyStringBefore)
       if(posi1<=0):
          print "ERROR finding posi1 "  
          return
       posi2 = fullPageText.find(keyStringAfter, posi1+1)
       debugLog( "posi2 is " + str(posi2))
       if(posi2<=0):
          print "ERROR finding posi2 " + fullPageText[posi1:]
          return
       
       deltaSkipKeyStringBefore = len(keyStringBefore)
       debugLog( "deltaSkipKeyStringBefore is " + str(deltaSkipKeyStringBefore))
       debugLog( "posi1+delta is " + str(posi1+deltaSkipKeyStringBefore))
       subString = fullPageText[posi1+deltaSkipKeyStringBefore:posi2]
       #subString = unicode(subString).encode("utf-8")
       #subString = unicode(subString)
       debugLog ( subString)
       return subString





 
 

def opLog(logtext):
   print logtext
   return

def debugLog(debugText):
   if (Debug): 
       print debugText

 
 


def checkDellMon34():
   pchecker = PriceChecker();

   OneMinute = 60
   oneHour = 60*OneMinute
   price = pchecker.keepChecking(dellMon34, oneHour)
   
   return 
 
def loadJsonFile(fname):
   
   fp = open(fname,"r")
   jsonData = json.load(fp )
   
   productList = []
   for key, value in jsonData.iteritems():
      tempProduct = Product(key, jsonData[key][Global.WebLinkKeyName], 
                                 jsonData[key][Global.OrigPriceKeyStringBeforeKeyName],jsonData[key][Global.OrigPriceKeyStringAfterKeyName], 
                                 jsonData[key][Global.SalePriceKeyStringBeforeKeyName],jsonData[key][Global.SalePriceKeyStringAfterKeyName])
      productList.append(tempProduct)

   return productList

def main():


   productList = loadJsonFile(DataFile)

   
   

   pchecker = PriceChecker();
   
   
   pchecker.setProductList(productList)
   pchecker.keepChecking(CheckInterval)

   

# end

main()



