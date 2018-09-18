



def test1():
    hex = b'\xfe'  # hex fe is dec 254
    print(hex)

    #
    print("convert a hex value to hex string : " + hex.hex())

    intvalue = int.from_bytes(hex, byteorder='big')  # or little

    print("int value is "+str(intvalue))



def test2():
    hex = b'\xff\xfe'  # hex ff fe is dec 65534
    print(hex)


    print("convert a hex value to hex string : " + hex.hex())  # print fffe

    intvalue = int.from_bytes(hex, byteorder='big')  # or little

    print("int value is "+str(intvalue))  #65534


def main():
    test1()
    print()
    test2()

main()
