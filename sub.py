import subprocess





def main():
   #subprocess.call(["ls", "-l"])

   command = "dir C:\\windows\\system32 /s"
   
   # stdout=subprocess.PIPE
   popen = subprocess.Popen(command, shell = True )
   #popen = subprocess.Popen(command)

   out, err = popen.communicate()
   print "command " + command
   #print "output " + str(out)
    
main()




#  for command in commands:
#           pipe.send("INFO-%s blackberry-signer is signing the bar file: "
#                     "\n'%s' \nwith command: \n'%s'" %
#                     (proc_name, bar_file, command))
#           print "sleeping"
#           time.sleep(20)
#           print "sleeping done"
#           print "Running command :  " + command
#           popen = subprocess.Popen(command, shell=True,
#               stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#           out, err = popen.communicate()
#           retcode = popen.wait()
#
#           if retcode: