

def funcA(a):
   print("funcA "+a)

def funcB(a,b):
   print("funcB "+str(a) + " " + str(b))

def funcC(a,b,c):
   print("funcC "+str(a) + " " + str(b) + " " + str(c))


def call_func(func, *arg):
   func(*arg)


def main():
   call_func(funcA, "AAA")
   call_func(funcB, "AAA", "BBB")
   call_func(funcC, "AAA", "BBB", "CCC")

main()

