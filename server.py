import socket
import threading
import sys

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = sys.argv[1]
ADDR = (SERVER, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
usernames = []

def broadcast(message):
    for client in clients:
        client.send(message.encode('utf-8'))

def handle_client(client, addr):
    print(f"[NEW CONNECTION] User with IP {addr[0]} connected.")

    connected = True
    try:
        username_len = client.recv(HEADER).decode(FORMAT)
        username_length = int(username_len)
        if username_length > 10:
            print("Invalid username!")
            client.close()
        username = client.recv(username_length).decode(FORMAT)
        usernames.append(username)
        clients.append(client)
        broadcast(f'{username} connected to the chatroom.')
        print(f'{username} just joined the room.')

    except:
        print("Problem with setting username!")
        client.close()

    try:
        while connected:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                broadcast(f"{username}: {msg}")
                client.send(msg.encode('utf-8'))
    except:
        index = clients.index(client)
        clients.remove(client)
        if username:
            print(f'{username} left the room.')
            username = usernames[index]
            usernames.remove(username)
            broadcast(f'{username} left the room.')
        else:
            print(f'User with IP {addr[0]} lost connection.')

    client.close()


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\n[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is listening...")
start()
