#!/usr/bin/python3

# Eventually this should deal with encryption among other practices as well as handling other ways processing incoming data

# import socket module
import socket

# create server socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define host and port
host = socket.gethostbyname('localhost')
port = 444

# bind socket to specified host and port
server_socket.bind((host, port))

# setup TCP listener
server_socket.listen(3)

# accept incoming connections, allowing up to 3 simultaneous connections
while True:
    clientsocket, address = server_socket.accept()
    
    # handle client connection
    print(f"received connection from: %s ") % str(address)
    
    # send response message
    message = 'Thank you for connecting to the server' + '\r\n'
    clientsocket.send(message.encode('ascii'))
    
    # close client socket
    clientsocket.close()

# socket - internal endpoint that sends and receives data
# works locally as internal

# afi net - specify protocol used for communication
    # ipv4 or ipv6
