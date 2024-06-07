def ToBinaryN(num):
    binary_positive = ToBinary(num, 6)
    binary_after_not = Not(binary_positive)
    add = 1
    negative_binary = ""
    for bit in binary_after_not:
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
    what_bit = int(2**index <= num)
    return str(what_bit) + ToBinary(num - 2**index*what_bit, index-1)


def Not(binary):
    final_binary = ""
    for bit in binary:
        final_binary += str(int(bit == "0"))
    return final_binary[::-1]


print(ToBinaryN(32))