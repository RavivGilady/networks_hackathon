import random
from socket import *
import asyncio
from struct import *
from datetime import datetime
import time
import threading

# from scapy.all import *
# HOST = get_if_addr("eth1")
HOST =gethostbyname(gethostname())
# HOST = '10.100.102.6'
PORT = 7578  # Port to listen on (non-privileged ports are > 1023)g
connections = [[], [], []]
waiting_for_connection_time=10
game_time = 10
buffer_size = 1024
def broadcast_invitation():
    broadcast_message = pack("!IcH", 0xfeedbeef, bytes({0x2}), PORT)
    for _ in range(10):
        cs = socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.bind((HOST, PORT))
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        cs.sendto(broadcast_message, ("<broadcast>", 13117))
        time.sleep(1)


def accept_connection():
    team_name = ""
    try:
        with socket(AF_INET, SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            s.settimeout(1.0)
            conn, addr = s.accept()
            while team_name == "":
                team_name = conn.recv(buffer_size).decode("UTF-8")
                connections[random.randint(1, 2)].append((team_name, conn, addr,[]))

    except:
        pass


async def initialize_game():
    start_time = datetime.now()

    print("Server started,\nlistening on IP address 172.1.0.135")
    offset=0
    while ((datetime.now() - start_time).seconds < waiting_for_connection_time):
        accept_connection()


def send_to_all_clients(message):
    for _,socket,_,_ in connections[1]:
        socket.send(message.encode())
    for _,socket,_,_ in connections[2]:
        socket.send(message.encode())

def construct_first_message():
    message="""Welcome to Keyboard Spamming Battle Royale.\n
Group 1:
==\n"""
    for team_name,_,_,_ in connections[1]:
        message+=team_name +"\n"
    message+= """\nGroup 2:
==\n"""
    for team_name,_,_,_ in connections[2]:
        message+=team_name +"\n"
    message+="\nStart pressing keys on your keyboard as fast as you can!!"
    return message

def start_threads():
    start_time=datetime.now()
    threads=[]
    for _, socket, _,chars in connections[1]:
        threads.append(threading.Thread(target=get_chars,args=(socket,chars,start_time)))
    for _, socket, _,chars in connections[2]:
        threads.append(threading.Thread(target=get_chars,args=(socket,chars,start_time)))
    for thread in threads:
        thread.start()
    # for thread in threads:
    #     thread.join()
    time.sleep(10)
def get_chars(server_socket,chars,start_time):
    while ((datetime.now() - start_time).seconds < game_time):
        data=""
        time=datetime.now()
        try:
            while (not data) and ((time - start_time).seconds < game_time):
                data = server_socket.recv(buffer_size).decode("UTF-8")
                time = datetime.now()
        except:
            pass

        chars.append(data)
def begin_game():
    first_message=construct_first_message()
    send_to_all_clients(first_message)
def construct_finish_message(group1,group2):
    winner=""
    winners=[]
    if(group1>group2):
        winner="Group 1"
        for con in connections[1]:
            winners.append(con[0])
    else:
        winner="Group 2"
        for con in connections[2]:
            winners.append(con[0])
    message="""Game over!
Group 1 typed in {} characters. Group 2 typed in {} characters.
{} wins!
Congratulations to the winners:
==\n""".format(group1,group2,winner)
    for team in winners:
        message+=team+"\n"
    return message
def finish_game():
    group1 = 0
    group2 = 0
    for _, _, _, chars in connections[1]:
        for strings in chars:
            group1+=len(strings)
    for _, _, _, chars in connections[2]:
        for strings in chars:
            group2+=len(strings)
    send_to_all_clients(construct_finish_message(group1,group2))
def main():
    x = threading.Thread(target=broadcast_invitation)
    x.start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_game())
    begin_game()
    start_threads()
    finish_game()
    print( "Game over, sending out offer requests...")

if __name__ == "__main__":
    main()
