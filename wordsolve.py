import time
import random
import sys

SFilename = "word_s.txt"    
#HFilename = "word_h.txt"    

# read file and return a list
def readFile(filename):
    fileobj = open(filename, 'r')
    list = fileobj.readlines()
    i=0
    
    # remove \n from each line
    for word in list :       
       word = word.strip()
       list[i]=word
       i+=1
       
    print " word lib has " + str( len(list)) +  " words"
    return list
    
      
def findWordsbyKey(list, index, char):
   outlist = []
   for word in list :      
      length = len(word)
      if(index<=length):
         if(word[index]==char):             
             outlist.append(word) 
   
   return outlist   


def findWordsbyLen(list, expectLen): 
   outlist = []
   for word in list :
       
      length = len(word)
      if(length == expectLen):
         outlist.append(word) 
   
   return outlist   


def printList(list):
   for word in list:
      print word

      
def main():
   fulllist = readFile(SFilename)     
   
   listChekLen =  findWordsbyLen(fulllist, 6)
   l5list = findWordsbyKey(listChekLen , 4, "l")
   printList (l5list)

   
main()
   











