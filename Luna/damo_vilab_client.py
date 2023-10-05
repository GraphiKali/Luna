import socket
import tqdm
import sys
from utilities import uniquify


def request_video(video_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('100.95.144.137', 8081))

    message = f"damo-vilab$r:{video_name}".encode('utf-8')
    client_socket.send(message)
    print(f"Request sent for video: {video_name}")

    image_info = client_socket.recv(4096).decode()
    parts = image_info.split("||")
    size = parts[0]
    filename = parts[1]
    print(f"Filename: {filename}")

    file_data = b""

    done = False

    progress_bar = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(size))

    while not done:
        data = client_socket.recv(4096)
        if file_data[-4:] == b"$end":
            done = True
        else:
            file_data += data
        progress_bar.update(4096)

    path = uniquify(f"./videos/{filename}")
    with open(path, "wb") as file:
        file.write(file_data)

    client_socket.close()


request_video(sys.argv[1])
