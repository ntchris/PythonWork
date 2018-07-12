import urllib
import urllib2
import time

def main():


  while True:   
    url="http:yourlink"
    
    url2="some times \ / is needed"
    url2 =  urllib.quote_plus(url2)
    
    
    print ("final url2 " + url2)
    
    f = urllib.urlopen(url)
    time.sleep(1)
    
    print f.read()
    
    time.sleep(2)

main()

