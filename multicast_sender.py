import socket
import sys

MCAST_GRP = sys.argv[1]
MCAST_PORT = 5007
MULTICAST_TTL = 2   


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

def login_set_up():
    login = input("Your login can has only 10 characters:\nEnter your login:")
    return login

if __name__ == "__main__":

    username = login_set_up(). rstrip()
    sock.sendto(f"{username} connected using multicast UDP".encode('utf-8'), (MCAST_GRP, MCAST_PORT))

    while True:
         MSG = input()
         if MSG == 'exit':
             sock.sendto(f"{username} left chatroom", (MCAST_GRP, MCAST_PORT))
             sock.close()
             break
         else:
             sock.sendto(f"{username}: {MSG}".encode('utf-8'), (MCAST_GRP, MCAST_PORT))

