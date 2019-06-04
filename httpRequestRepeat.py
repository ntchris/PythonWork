import urllib
import urllib2
import time

def main():


  while True:   
    url="https://polls.polldaddy.com/vote-js.php?p=10053553&b=1&a=46114414,&o=&va=16&cookie=0&n=4789327394|792&url=https%3A//www.thestar.com/news/queenspark/2018/07/11/ontario-students-will-be-taught-the-old-sex-ed-curriculum-when-they-go-back-to-school-education-minister-says.html"
    
    url="https://polls.polldaddy.com/vote-js.php?p=10053553&b=1&a=46114414,&o=&va=16&cookie=0&n=3ccb9b3dcc|389"
        
    url="https://polls.polldaddy.com/vote-js.php?p=10053553&b=1&a=46114414,&o=&va=16&cookie=0&n=3ccb9b3dcc|634&url=https%3A//www.thestar.com/news/queenspark/2018/07/11/ontario-students-will-be-taught-the-old-sex-ed-curriculum-when-they-go-back-to-school-education-minister-says.html"
    
    url2="some times \ / is needed"
    url2 =  urllib.quote_plus(url2)
    
    
    print ("final url2 " + url)
    
    f = urllib.urlopen(url)
    time.sleep(1)
    
    print f.read()
    
    time.sleep(2)

main()

