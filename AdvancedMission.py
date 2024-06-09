XOR_NUM = 5

def encryption_of_file(file_name):
    lst_file = list(file_name)
    print(lst_file)
    for index,char in enumerate(lst_file):
        encrypted_char = chr(ord(char) ^ XOR_NUM)
        lst_file[index] = encrypted_char
    encrypt_file = "".join(lst_file)
    return encrypt_file

if __name__ == "__main__":
    file_name = input("Enter the name of the file\n")
    encrypt_file = encryption_of_file(file_name)
    print(encrypt_file)



