import socket
import select
import sys

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 4:
    print("Correct usage: script, Name, IP address, port number")
    exit()

# Store the client's name, server IP address, and port number from command-line arguments
Name = str(sys.argv[1])
IP_address = str(sys.argv[2])
Port = int(sys.argv[3])  # Convert the port number to an integer

# Create a TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server using the provided IP address and port number
client.connect((IP_address, Port))

while True:
    # Maintain a list of possible input streams
    sockets_list = [sys.stdin, client]

    # Use select to monitor the input streams for readiness
    read_sockets, _, _ = select.select(sockets_list, [], [])

    # Iterate over the list of sockets that are ready for reading
    for socks in read_sockets:
        # If the client socket is ready, receive and print the message
        if socks == client:
            message = socks.recv(2048)
            if message:
                print(message.decode("utf-8"))
            else:
                # If the server has closed the connection
                print("Disconnected from chat server")
                client.close()
                exit()
        # If the standard input is ready, read the message, send it to the server, and print it
        else:
            message = sys.stdin.readline()
            client.send(bytes(f"<{Name}>: {message.strip()}", "utf-8"))
            print(f"<You>: {message.strip()}")
