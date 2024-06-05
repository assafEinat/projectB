def ToBinaryN(num):
    binary_positive = ToBinary(num, 6)
    binary_after_not = Not(binary_positive)
    add = 1
    negative_binary = ""
    for num in binary_after_not[::-1]:
        if add == 1:
            if num == "1":
                negative_binary = "0" + negative_binary
            else:
                negative_binary = "1" + negative_binary
                add = 0
        else:
            if num == "1":
                negative_binary = "1" + negative_binary
            else:
                negative_binary = "0" + negative_binary
    negative_binary = "1" + negative_binary
    return negative_binary


def ToBinary(num, index):
    if index == -1:
        return ""
    if 2**index <= num:
        return "1" + ToBinary(num - 2**index, index-1)
    return "0" + ToBinary(num, index - 1)


def Not(binary):
    final_binary = ""
    for num in binary:
        if num == "0":
            final_binary += "1"
        else:
            final_binary += "0"
    return final_binary


print(ToBinaryN(32))