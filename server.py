import socket
import threading
import time

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []

def handle_client(client_socket, client_number):
    global clients
    try:
        if client_number == 0:
            print(f"Madeline connected")
        elif client_number == 1:
            print(f"Badeline connected")


        # You can do something with the client data here

    except Exception as e:
        print(f"Error handling client {client_number}: {str(e)}")


def await_players():
    server_socket.settimeout(5)
    while True:
        try:
            client_socket, addr = server_socket.accept()
            clients.append(client_socket)

            handle_client(client_socket, len(clients) - 1)
        except socket.timeout:
            break
    

await_players()

for socket in clients:
    print(socket)



