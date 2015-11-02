'''
Training1
 
unzip tool
 
 
Created on May 03, 2011
@author: Chris Jiang
'''
import re
import sys
import os 
import fnmatch
import glob
import zipfile

 
 
# Show the Help text
def showHelp(): 
  print( " unzip.py archive.zip file-to-extract" )
  

# end of Show the Help text
 
# ===========================================================
# process the given files list for pattern.
def unzip (fname, ftoextract ):
    
    myzipfile = zipfile.ZipFile( fname)
    #print( myzipfile.namelist())
    myzipfile.extract (ftoextract )  
    return 0
    
# def unzip (fname, ftoextract ):
    
 
 
 
# ==================================================
# 
#  
def isValidArg (arglist):   
    
    if ( len(arglist ) ==2 ):       
        return True
    showHelp() 
    return False  #
# end of def validateInput ():


 
# ========================================================
# Main Function starts
# ========================================================
 
 
###  d:\temp\abc.zip  hint.jpg
 
###############################################################################
 
def main(arglist):
    """
    The main method for this application.
    The ``arglist`` parameter must be a list of strings to use as the
    command-line arguments.
    Returns an integer to be used as the exit status: 0 on success,
    1 on failure, 2 if invalid command-line arguments specified
    """
 
     
   
    if( not isValidArg( arglist) ):
        return 1
    
    # input is good, continue process:
    zipfile = arglist[0]
    filetoextract = arglist[1]
    
   
    r = unzip( zipfile , filetoextract )
    print ( r)
    return (r)
   
###############################################################################
     

isPrintDebugInfo = False
printLineNOAndTextLine = False
if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
       
 
 
     
    
  
 
 
 
###############################################################################
 
 
 
 
 
