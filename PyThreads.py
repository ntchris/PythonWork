'''
PyThread
  
 
Created on May 3, 2011
@author: Chris Jiang
'''
import re
import sys
import os 
import fnmatch
import glob
import string
 
# Show the Help text
def showHelp(): 
    helpText = " search  path  Nlargestfiles";
    print(helpText)

# end of Show the Help text
 
# 
  

def checkdir( path ):
    print('not found')
    pass
      
     
    
 
  
def searchPathAndFiles (path, N): 
    for  basedir, listdirs, listfiles in os.walk(path):  
       for f in listfiles :
           r = checkandappendfile(  basedir+"\\"+f , N )   
    
    NLargestFileList.sort(reverse=True)
    return r
 
 
   
# ========================================================
# Main Function starts
# ========================================================
 
 
###############################################################################
 
def main(arglist):
    """
    The main method for this application.
    The ``arglist`` parameter must be a list of strings to use as the
    command-line arguments.
    Returns an integer to be used as the exit status: 0 on success,
    1 on failure, 2 if invalid command-line arguments specified
    """
 
    if (len(arglist) == 0) :
        # we really should display the help text if no arg is given
        # showHelp()  just to make the unit test happy
        sys.stderr.write("no argument input error")
        return 2;
    
    
    # input is good, continue process:
    searchpath = arglist[0]
     
    NlargestFile = int(  arglist[1] )   
    
    if(not os.path.isdir(searchpath)):
        return 1
     
    r = searchPathAndFiles(searchpath , NlargestFile)   
  
    for f in NLargestFileList:
        print (f)
    
    return (r)
   
###############################################################################
     
NLargestFileList =  list()
 


isPrintDebugInfo = False
printLineNOAndTextLine = False
if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
       
 
 
     
     
 
