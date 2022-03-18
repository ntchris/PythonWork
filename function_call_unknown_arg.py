



def funcA(a):
   print("funcA "+a)

def funcB(a,b):
   print("funcB "+str(a) + " " + str(b))

def funcC(a,b,c):
   print("funcC "+str(a) + " " + str(b) + " " + str(c))


def retry_func(func, *arg):
   print("calling " + func.__name__ )
   func(*arg)


def main():
   retry_func(funcA, "AAA")
   retry_func(funcB, "AAA", "BBB")
   retry_func(funcC, "AAA", "BBB", "CCC")

main()
