import sys, getopt

def change(list):
   print (list);
   list = [1,2,3];
   print (list);
   return
   
list0 = [3,5,6];   
change(list0)
print (list0);

for letter in 'Python': # First Example 
   print ('Current Letter :', letter)



#def main(argv):
tinydict = {'name': 'john','code':6734, 'dept': 'sales'}
dict = {} 
dict['one'] = "This is one" 
dict[2] = "This is two"
dict["name"] = "name value"
print(dict)
print(tinydict.keys())
num = input("Enter a number :")

print (num)


argv = sys.argv[1:]
print  ('Argument List:', argv)
option1Arg =''
option2Arg =""
option1 = "-a"
option2 = "-b"
try:
  opts, args = getopt.getopt(argv,"a:b:")
except getopt.GetoptError:
  print ("err")
  sys.exit(2)
for opt, arg in opts:  
  print(opt,arg)
  if opt == option1:
     option1Arg = arg
  elif opt == option2:
     option2Arg = arg

print(option1, option1Arg, option2, option2Arg)