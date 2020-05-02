# change the game name from name to file name
# so we know which file is that game.

import re
import os
import sys
import time
import json
import string
import gzip

import xml.etree.ElementTree as ET

class Constants:
  gameList = "gameList"
  path = "path"
  name = "name"
  pathIndex=0
  nameIndex=1
    
class RetropieGamelistNameChanger:
   def __init__(self ):
      return 
   
   def changeGameNameByIndex(self, node ):

      # using find would be future proof
      path = node[Constants.pathIndex].text  
      name = node[Constants.nameIndex]  
      
      filename = os.path.basename(path)
      new_name = filename + ": " + name.text
      print(new_name + " "  )

      name.text = new_name

      return

   def processFile(self, filename):
       print(filename)
       tree = ET.parse(filename)
       root = tree.getroot()
       if( Constants.gameList != root.tag):
          print("this is not a gamelist xml file, it should have a "+ Constants.gameList+ " root ")
          print(root.tag)
          return

       for game in root:
          self.changeGameNameByIndex(game)          
       tree.write(filename)      
       return

def main():
   changer = RetropieGamelistNameChanger()
   fname = "d:\\gamelist.xml"
   changer.processFile(fname)


main()
