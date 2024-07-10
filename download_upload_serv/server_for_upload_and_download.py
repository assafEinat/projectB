import socket
import os

NAME_MAX = 4
DATA_MAX = 8
OPTION_MAX = 1

def receive_all(sock, length):
    data = bytearray()
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def handle_upload(client_socket):
    size_len = int(receive_all(client_socket, DATA_MAX).decode())
    data_size = int(receive_all(client_socket, size_len).decode())
    file_data = receive_all(client_socket, data_size)
    name_len = int(receive_all(client_socket, NAME_MAX).decode())
    name = receive_all(client_socket, name_len).decode()

    
    directory = 'server_files'
    os.makedirs(directory, exist_ok=True)

    path = os.path.join(directory,name)
    with open(path, 'wb') as new_file:
        new_file.write(file_data)

def handle_download(client_socket):
    name_len = int(receive_all(client_socket, NAME_MAX).decode())
    name = receive_all(client_socket, name_len).decode()
    path = os.path.join("server_files", name)
    if os.path.exists(path):
        data_to_send = bytearray()
        with open(path, 'rb') as file:
            data_to_send.extend(file.read())
        os.remove(path)
        data_len = str(len(data_to_send)).zfill(DATA_MAX).encode()
        client_socket.send(data_len)
        client_socket.send(data_to_send)
    else:
        message = "the file you wanted to download does not exist"
        message_len = str(len(message)).zfill(DATA_MAX).encode()
        client_socket.send(message_len)
        client_socket.send(message.encode())

def main():
    server_address = ('0.0.0.0', 12345)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen()
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            try:
                while True:
                    option_len = int(receive_all(client_socket, OPTION_MAX).decode())
                    option = receive_all(client_socket, option_len).decode()
                    if option == "upload":
                        handle_upload(client_socket)
                    elif option == "download":
                        handle_download(client_socket)
            except Exception as e:
                print(f"Error handling client: {e}")
            finally:
                client_socket.close()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
