import socket
import threading
import sys
import struct

PORT = 5050
SERVER = sys.argv[1]
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# TCP SOCKET
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# UDP SOCKET -> MULTICAST
MCAST_GRP = sys.argv[2]
MCAST_PORT = 5007
IS_ALL_GROUPS = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if IS_ALL_GROUPS:
  sock.bind(('', MCAST_PORT))
else:
  sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def send():
    while True:
        try:
            msg = input()
            message = msg.encode(FORMAT)
            send_length = str(len(message)).encode(FORMAT)
            client.send(send_length)
            client.send(message)
        except:
            print('Lost connection with server!')
            break

def send_nickname(msg):
    message = msg.encode(FORMAT)
    send_length = str(len(message)).encode(FORMAT)
    client.send(send_length)
    client.send(message)


def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'exit':
                client.close()
                break

            if len(message) != 0:
                print(message)
        except:
            print('An error occurred.')
            client.close()
            break


def login_set_up():
    login = input("Your login can has only 10 characters:\nEnter your login:")
    return login

def multicast_receive():
    while True:
        try:
            multicast_msg = sock.recv(1024).decode('utf-8')
            if multicast_msg != "":
                print(multicast_msg)
        except:
            pass


if __name__ == "__main__":

    # LOGIN SET
    username = login_set_up()
    send_nickname(username)

    # First thread for receving data from TCP socket
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    # Seocnd thread for sending data to server TCP
    send_thread = threading.Thread(target=send)
    send_thread.start()

    # Third thread for receving data from UDP Multicast
    receive_multicast = threading.Thread(target=multicast_receive)
    receive_multicast.start()


