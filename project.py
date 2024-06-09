BITS_NEEDED = 8


def ToBinaryN(num):
    index = num.bit_length()
    binary_positive_and_not = ToBinary(num, BITS_NEEDED-2)
    add = 1
    negative_binary = ""
    for bit in binary_positive_and_not[::-1]:
        if add == 1:
            if bit == "1":
                negative_binary = "0" + negative_binary
            else:
                negative_binary = "1" + negative_binary
                add = 0
        else:
            negative_binary = bit + negative_binary
            
    negative_binary = "1" + negative_binary
    return negative_binary


def ToBinary(num, index):
    if index == -1:
        return ""
    what_bit = pow(2,index) <= num
    return str(int(not what_bit)) + ToBinary(num - 2**index*int(what_bit), index-1)

if __name__ =="__main__":
    print(ToBinaryN(34))


