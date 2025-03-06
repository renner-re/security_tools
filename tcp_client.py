#!/usr/bin/python3
# Eventually this should deal with encryption among other practices as well as handling other ways processing incoming data.

import socket

# define host and port
host = '192.168.1.104'
port = 444

try:
    # create a socket object and establish a connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # send request to server (if needed)
    # client_socket.send(b'Hello, server!')

    # receive and print response
    message = client_socket.recv(1024)
    print(message.decode('ascii'))

except socket.error as e:
    print(f"Socket error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # close the socket in a finally block to ensure cleanup
    if 'client_socket' in locals():
        client_socket.close()
