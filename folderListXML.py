import os
import codecs
import sys
import xml.etree.ElementTree as ET
#For pretty format
import xml.dom.minidom

errorList =  []

class Const(object):
   Attr_FileName = "file_name"
   Attr_FileSize = "file_size"
   Attr_FileType = "file_type"
   Attr_FolderName = "folder_name"   
   Attr_FolderSizeSubTotal = "folder_size_subtotal"
   Attr_FolderSizeTotal = "folder_size_total"
   Tag_Folder = "folder"


    
########################################################################################
#
#  XML work
#
########################################################################################
def recurse_traverFolder(parentNode, toAddFullPath):
   
   #print "recurse checking path: " + toAddFullPath.encode("utf-8")
   current_folder_name = os.path.basename(toAddFullPath)
   #If this is root, the current folder name is empty
   if(current_folder_name == ""):
       current_folder_name = toAddFullPath
   currentFolderNode = addFolderNode(parentNode, current_folder_name)
   currentFolderNode.attrib[Const.Attr_FolderSizeSubTotal] = "0"
   currentFolderNode.attrib[Const.Attr_FolderSizeTotal] = "0"


   try:
      # very important to use unicode(path)
      obj = os.walk(unicode(toAddFullPath))
      tuples = next(obj)
   except Exception as e:
      print("Error accessing: " + toAddFullPath.encode("utf-8"))
      errorList.append(e)
      print(errorList)
      print("return ")
      # something is wrong, no access ? fake folder? return current node as is
      return currentFolderNode

   dirpath=unicode(tuples[0])
   dirnames = tuples[1]
   filenames = tuples[2]  

   #The sub total size of one folder, including all files and all sub-dirs
   totalFolderSize = 0
   #subtotal, only include files in current dir, but not include subdirs.
   subtotalFolderSize = 0

   #Deal with all subdir in current folder
   for subdir in dirnames:
      fullSubdirPath = os.path.join(dirpath, subdir)
      tempFolderNode = recurse_traverFolder(currentFolderNode, fullSubdirPath)
      #print "checking path " + fullSubdirPath.encode("utf-8")
      #print "checking node " + (tempFolderNode.attrib[Const.Attr_FolderName]).encode("utf-8")
      #print "size iszzz " + tempFolderNode.attrib[Const.Attr_FolderSizeTotal]
      #print "tempFolderNode is " + str(tempFolderNode)
      totalFolderSize += int(tempFolderNode.attrib[Const.Attr_FolderSizeTotal])
   
   #Deal with all files in current folder       
   for f in filenames:
         tempfullpathfilename = os.path.join(dirpath, f)
         tempFileNode = addFileNode(currentFolderNode, tempfullpathfilename)
         #all file size in current dir 
         subtotalFolderSize += int(tempFileNode.attrib[Const.Attr_FileSize])

   #including all subdir size and files in current dir
   totalFolderSize += subtotalFolderSize

   currentFolderNode.attrib[Const.Attr_FolderSizeSubTotal] = str(subtotalFolderSize)
   currentFolderNode.attrib[Const.Attr_FolderSizeTotal] = str(totalFolderSize)

   return currentFolderNode

   


def addFolderNode(parentNode, subDir):
   #one file is one node
   #current_dirname = os.path.basename(fullpath)
   tempFolderNode = ET.SubElement(parentNode, Const.Tag_Folder)

   tempFolderNode.attrib[Const.Attr_FolderName] = subDir
   #tempFolderNode.attrib[Const.Attr_FolderSizeTotal] = "0"
   return tempFolderNode

def addFileNode(parentNode, fullPathFilename):

   #print "checking file " + fullPathFilename.encode("utf-8")
   # one file is one node
   tempFilerNode = ET.SubElement(parentNode, "file")
   filename = os.path.basename(fullPathFilename)
   fileExt = os.path.splitext(filename)[1]
    
   tempFilerNode.attrib[Const.Attr_FileName] = filename
   tempFilerNode.attrib[Const.Attr_FileType] = fileExt

   size = os.path.getsize(fullPathFilename)
   tempFilerNode.attrib[Const.Attr_FileSize] = str(size)
   return tempFilerNode



def writePrettyTextFile(tree):
   
   #tree.write("test.xml", encoding="UTF-8", xml_declaration=True)
   root = tree.getroot()
   xmltext = ET.tostring(root)
   tempXmlObj = xml.dom.minidom.parseString(xmltext)
   
   prettyText = tempXmlObj.toprettyxml(indent="   ", newl='\n')
   prettyText = prettyText.encode("utf-8")
   
   file = open("outputfile.xml", "w")
   file.write(prettyText)
   file.close


def startTraverFolder(workPath):

   _root = ET.Element("FileList")

   recurse_traverFolder(_root, workPath)
   # wrap it in an ElementTree instance, and save as XML
   tree = ET.ElementTree(_root)
   writePrettyTextFile(tree)


def getDirInfo():
   if(len(sys.argv)<=1):
      #workPath = "d:\\temp"
      #workPath = "Documents and Settings"
      workPath = "\\\\?\\"+"c:\\P4\\dev\\ate\\projects\\api\\testing\\7.0.0\\JavaATTD\\scripts\\SCMBuild\\bin\\tmp"
      #workPath = "c:\\P4\\dev\\ate\\projects\\api\\testing\\7.0.0\\JavaATTD\\scripts\\SCMBuild\\bin\\tmp\\"
   else:
      workPath = sys.argv[1]
      if(workPath==""):
         workPath = "d:\\temp"

   print("checking path " + workPath)

   startTraverFolder("\\\\?\\"+ workPath)


def testParse(xmlFile):
   tree = ET.parse(xmlFile)
   #return tree
   writePrettyTextFile(tree)


def main():
   getDirInfo()
   #testParse("test.xml")



main()

# end of file