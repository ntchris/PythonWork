import sys



def readFile(fileName):

    lineList = []
    try:
       fileObj = open(fileName, "r")
    except IOError as fileOpenError:
       return fileOpenError

    for origline in fileObj:

       # do not strip and skip empty lines, we need the correct index map to the text file
       lineList.append(origline)

    fileObj.close()
    return lineList


def lineToHex(line):
    
    string = ""
    for char in line:
       # remove 0x ,  0x12 -->12  0xAB --> AB
       #string = string + hex(ord(char)) [2:] + " "
       #hexstring = "{:02x}".format(char)
       hexstring = char.encode("hex")
       string = string + hexstring + " "


   
    return string



def main():
   filename = sys.argv[1]

   lineList = readFile(filename)
   hexstring = ""
   size = len(lineList)
   i=0
   for line in lineList :
      print("i="+str(i)+" size="+str(size))
     

      if((i+1) ==size):
         # remove the strange last a at end of the file
         line = line.strip()
      i=i+1    
      hexstring = hexstring + lineToHex(line)

   print hexstring




main()


