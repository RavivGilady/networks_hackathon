from socket import *
import asyncio
from struct import *
from datetime import datetime
connection_port=7578
connections = [[], [], []]

async def broadcast_invitation():
    broadcast_message = pack("!IcH", 0xfeedbeef, bytes({0x2}), connection_port)
    await asyncio.sleep(1)
    cs = socket(AF_INET, SOCK_DGRAM)
    cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    cs.sendto(broadcast_message, ("<broadcast>", 13117))


async def accept_connection():
    pass


async def get_connections():
    
    pass


def main():
    start_time = datetime.now()
    print("“Server started,\nlistening on IP address 172.1.0.135”")
    for _ in range(10):
        asyncio.run(broadcast_invitation())
    while():
        try:
            await asyncio.wait_for(get_connections, timeout=5)

        except asyncio.TimeoutError:
            pass
