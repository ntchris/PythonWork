import os
import codecs
import sys

errorList =  []

def get_dir_size(start_path = u'd:/temp'):
    
    if not os.access(start_path, os.R_OK):
       errorList.append("path doesn't exist , or no read access")
       return
    
    
    try:
       obj=(os.walk(start_path))

       tuples = next(obj)
      
    except Exception as e:
       errorList.append(e)
       return 0
       
    dirpath=tuples[0]
    dirnames = tuples[1]
    filenames = tuples[2] 
    
    all_file_size =0
    all_dir_size = 0
     
    
    # print "dirpath " , dirpath
    # print "dirnames ", dirnames
    # print "filenames ", filenames
    
    #sum up all files' size    
    for f in filenames:
        fullpath = os.path.join(dirpath, f)
        if(len(fullpath)<=255):
           # toooo long , ignore
           # all_file_size +=0                   
           try:
              all_file_size += os.path.getsize(fullpath)
           except Exception as e:              
              errorList.append(e)
    #print "all file size is ", all_file_size
      
    all_dir_size = 0
    for subdir in dirnames:
       fullsubdir = os.path.join(dirpath, subdir)
       all_dir_size += get_dir_size(fullsubdir)
    
    #print "all dir size is ", all_dir_size
    
    total_size = all_file_size + all_dir_size
    
    # if folder is less than xxx kb then ignore it
    if(total_size/1024 >500):
    
    
       print "\""+ start_path + "\", " + str( total_size/1024)
    
    return total_size 

    
    
def get_dir_size2(start_path = u'd:/temp'):
    
    i=0
    gen = os.walk(start_path)
    print gen.next()
    print gen.next()
    print gen.next()
    print gen.next()
    # for path, dirs, files in (os.walk(start_path)) :
       
       # i=i+1;
       # print i
       # print "path ", path
    
        
    
    # print next(tuples)
    
def main():

   workPath = sys.argv[1]
   if(workPath==""):
      workPath = u"D:\\temp"
      
   print "checking path " + workPath
   
   longFile = "d:\\StateStore\\USMT\\File\\D$\\p4\\dev\\ate\\projects\\devicetest\\projects\\6.1.0\\JavaAPI\\Runtime\\sqa\\tests\\net\\rim\\device\\api\\servicebook\\ServiceBook_DuplicateSecureServiceException\\sqa_tests_net_rim_device_api_servicebook_ServiceBook_DuplicateSecureServiceException.jdp" 
   #print longFile 
   #print "size is" , os.path.getsize(longFile)
   
   #get_dir_size2(u"D:/testsize/")
   
   print ("Path , Size(KB)")
   
   get_dir_size(workPath) 
   
   #print errorList;
   

#get_dir_size(u"c:\Documents and Settings")


main()