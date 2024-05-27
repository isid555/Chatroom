import socket
import select
import sys
from threading import Thread

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

# Store the server IP address and port number from command-line arguments
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])  # Convert the port number to an integer

# Bind the socket to the address and port
server.bind((IP_address, Port))

# Listen for incoming connections (maximum of 1000 connections)
server.listen(1000)
print(f"Server started at IP {IP_address} on port {Port}")

list_of_clients = []

def clientthread(conn, addr):
    # Send a welcome message to the connected client
    conn.send(bytes("Welcome to this chatroom!", "utf-8"))
    print(f"{addr[0]} connected to the chatroom")

    while True:
        try:
            message = conn.recv(2048)
            if message:
                print(f"{addr[0]}: {message.decode('utf-8')}")
                # Broadcast the message to all other clients
                broadcast(message, conn)
            else:
                # Remove the client if the message is empty
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                # Remove the client if the link is broken
                remove(client)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    # Accept a new connection
    conn, addr = server.accept()
    list_of_clients.append(conn)
    # print(f"{addr[0]} connected")

    # Create a new thread for the client
    Thread(target=clientthread, args=(conn, addr)).start()

conn.close()
server.close()
