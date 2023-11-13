import socket
import pygame
import sys

# Client configuration
HOST = '127.0.0.1'
PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

pygame.init()

# Your Pygame initialization code goes here

try:
    # Receive the identification message from the server
    identification_message = client_socket.recv(1024).decode('utf-8')
    print(identification_message)

    # Your Pygame game loop goes here

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    client_socket.close()
    pygame.quit()
    sys.exit()