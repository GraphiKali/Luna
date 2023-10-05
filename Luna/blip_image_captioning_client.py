import os
import socket
import sys
import time


def request_image(img_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('your host here', 8082))
    
    with open(img_path, "rb") as file:
        file_size = os.path.getsize(img_path)
        data = file.read()

    message = f"{file_size}".encode('utf-8')
    client_socket.send(message)

    client_socket.sendall(data)
    client_socket.send(b"$end")

    caption = client_socket.recv(4096).decode()
    print(caption)

    client_socket.close()

try:
    request_image(sys.argv[1])
except:
    request_image(r".\images\a mountain range.png")
