import socket
import time
from struct import *

UDP_IP =socket.gethostbyname(socket.gethostname())

UDP_PORT = 13117
buffer_size = 1024


def scan():
    server_addr = ""
    print("Client started, listening for offer requests...")

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while server_addr == "":
        data, host = sock.recvfrom(buffer_size)  # buffer size is 1024 bytes
        address, socket_num = host
        if data[0:5] == b'\xfe\xed\xbe\xef\x02':
            return address, int.from_bytes(data[5:], "big")


def connect(server_address, server_port):
    print("Received offer from %s,attempting to connect... " % server_address)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_address, server_port))
    return s


def send_team_name(socket_to_server):
    team_name = "Raviv Gilady"
    socket_to_server.send(team_name.encode())


server_address, server_port = scan()
socket_to_server = connect(server_address, server_port)
send_team_name(socket_to_server)
time.sleep(10)
print(socket_to_server.recv(buffer_size).decode("UTF-8"))
socket_to_server.send("raviv".encode())
time.sleep(10)
print(socket_to_server.recv(buffer_size).decode("UTF-8"))
# I finished my code here. I know that I don't get input from user & send it. Unfortunately I couldn't make it on time.
