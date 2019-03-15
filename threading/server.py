import socket
import threading


sockets = {}
addresses = {}
HOST = "localhost"
PORT = 8888
ADDRESS = (HOST, PORT)
BUFFER = 2048
#PASSWORD = "123"


# Function to handle connection requests, without authentication at this time
def handle_requests():
    # While loop to accept all connection requests
    while True:
        client_socket, client_address = server_socket.accept()
        # print("# %s:%s has connected!" % client_address)
        addresses[client_socket] = client_address
        print("# %s has connected!" % str(addresses.get(client_address)))
        threading.Thread(target=handle_messages, args=(client_socket,)).start()


# Function to receive messages from client, then forward them to chat room
def handle_messages(client_socket):
    # Get username from client
    name = client_socket.recv(BUFFER).decode()
    # Send welcome message from server to new client
    welcome = '# Welcome %s to VERA chat room! Type "quit" and press Enter to exit this program.' % name
    client_socket.send(welcome.encode())
    # Send a broadcast notification about new client into chat room
    hello = "# User %s has joined our chat room." % name
    broadcast_notification(hello, client_socket)
    sockets[client_socket] = name
    while True:
        message = client_socket.recv(BUFFER).decode()
        if message != "quit":
            broadcast_message(name, message, client_socket)
        else:
            print("# %s has disconnected." % str(addresses.get(client_socket)))
            client_socket.close()
            sockets.pop(client_socket)
            # del sockets[client_socket]
            goodbye = "# User %s has left from our chat room." % name
            broadcast_notification(goodbye, client_socket)
            break


# Function to send broadcast messages to all connected clients, except sender
def broadcast_message(name, message, client_socket):
    for s in sockets:
        if s != client_socket:
            s.send(("[" + name + "]: " + message).encode())


# Function to send broadcast system notifications to all connected clients, except sender
def broadcast_notification(notification, client_socket):
    for s in sockets:
        if s != client_socket:
            s.send(notification.encode())


if __name__ == "__main__":
    print("   ____   ____                      \n"
          "   \   \ /   / ____ _______ _____   \n"
          "    \   Y   /_/ __ \\\_  __ \\\__  \  \n"
          "     \     / \  ___/ |  | \/ / __ \_\n"
          "      \___/   \___  >|__|   (____  /\n"
          "                  \/             \/ \n"
          'VERA v1.0 | March 2019 | NTH347 | "Passion is power"\n')

    # Create server socket and enable re-use feature on the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind socket to address and listen for incoming connection
    server_socket.bind(ADDRESS)
    server_socket.listen(10)
    print("# VERA server running on {}:{}".format(HOST, PORT))
    accept_thread = threading.Thread(target=handle_requests)
    accept_thread.start()
    # accept_thread.join()
    # server_socket.close()
