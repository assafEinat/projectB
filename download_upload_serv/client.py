import socket
import os

NAME_MAX = 4
DATA_MAX = 8
OPTION_MAX = 1

def send_all(sock, data):
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent

def upload_file(client_socket, file_path):
    print(file_path)
    if not os.path.exists(file_path):
        print("File does not exist")
        return

    with open(file_path, 'rb') as file:
        file_data = file.read()

    file_name = os.path.basename(file_path)
    file_name_encoded = file_name.encode()
    file_name_len = str(len(file_name_encoded)).zfill(NAME_MAX).encode()
    data_size = str(len(file_data)).zfill(DATA_MAX).encode()

    send_all(client_socket, str(len("upload")).zfill(OPTION_MAX).encode())
    send_all(client_socket, "upload".encode())
    send_all(client_socket, str(len(data_size)).zfill(DATA_MAX).encode())
    send_all(client_socket, data_size)
    send_all(client_socket, file_data)
    send_all(client_socket, file_name_len)
    send_all(client_socket, file_name_encoded)

def download_file(client_socket, file_name):
    file_name_encoded = file_name.encode()
    file_name_len = str(len(file_name_encoded)).zfill(NAME_MAX).encode()

    send_all(client_socket, str(len("download")).zfill(OPTION_MAX).encode())
    send_all(client_socket, "download".encode())
    send_all(client_socket, file_name_len)
    send_all(client_socket, file_name_encoded)

    data_size = int(client_socket.recv(DATA_MAX).decode()) 
    data = receive_all(client_socket, data_size)

    if data.startswith(b'the file you wanted to download does not exist'):
        print(data.decode())
    else:
        directory ='client_files'
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join('client_files', file_name), 'wb') as file:
            file.write(data)
        print(f"{file_name} downloaded successfully.")

def receive_all(sock, length):
    data = bytearray()
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def main():
    server_address = ('127.0.0.1', 12345)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    try:
        while True:
            option = input("Enter 'upload' to upload a file or 'download' to download a file (or 'exit' to quit): ").strip().lower()
            if option == "upload":
                file_path = input("Enter the path of the file to upload: ").strip()
                print("nigger")
                print(file_path)
                upload_file(client_socket, file_path)
            elif option == "download":
                file_name = input("Enter the name of the file to download: ").strip()
                download_file(client_socket, file_name)
            elif option == "exit":
                break
            else:
                print("Invalid option, please try again.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
