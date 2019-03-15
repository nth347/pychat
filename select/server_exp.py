import socket, select, sys, os
from color import *
from configparser import ConfigParser
import ast

# Read configuration file and get its arguments
parser = ConfigParser()
parser.read("config.cfg")
HOST = parser.get("serverconfig", "HOST")
PORT = int(parser.get("serverconfig", "PORT"))
SERVER_ADDRESS = (HOST, PORT)
BUFFER = int(parser.get("serverconfig", "BUFFER"))
MONITOR = ast.literal_eval(parser.get("serverconfig", "MONITOR"))

INPUTS = []
OUTPUTS = []
ERRORS = []
socket_to_username = {}     # keys are sockets, values are usernames
socket_to_address = {}      # keys are sockets, values are addresses in tuple format (hostname, port)
# CURSOR_UP = "\x1b[1A"
# CLEAR_LINE = "\x1b[2K"
WIDTH = os.get_terminal_size().columns

os.system("clear")
print(fg.GREEN, style.BRIGHT)

print("   ____   ____                      ".center(WIDTH))
print("   \   \ /   / ____ _______ _____   ".center(WIDTH))
print("    \   Y   /_/ __ \\\_  __ \\\__  \  ".center(WIDTH))
print("     \     / \  ___/ |  | \/ / __ \_".center(WIDTH))
print("      \___/   \___  >|__|   (____  /".center(WIDTH))
print("                  \/             \/ ".center(WIDTH))
print("VERA v1.0 | March 2019 | NTH347 | Passion is power\n".center(WIDTH))

print(style.RESET_ALL)
print(fg.BLUE, style.BRIGHT)
def chat_server():
    # Create server socket on server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable re-use address feature on the socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to address and listen for connection requests
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(10)
    # Add server socket object to the list of readable connection
    INPUTS.append(server_socket)    # INPUTS = [server_socket]
    print("VERA server running on {}\n".format(SERVER_ADDRESS))
    while True:
        readable, writable, exceptional = select.select(INPUTS, OUTPUTS, ERRORS, 0)
        for s in readable:
            # If there is the server socket in INPUTS, it means that a new client has arrived,
            # therefore, it calls accept() and adds a returned socket to INPUTS
            if s is server_socket:  # s == server_socket
                client_socket, client_address = server_socket.accept()
                INPUTS.append(client_socket)
                # Receive username of the new client
                if client_socket not in socket_to_username:
                    username = client_socket.recv(BUFFER).decode()
                    socket_to_username[client_socket] = username
                # Add address to list socket_to_address
                if client_socket not in socket_to_address:
                    socket_to_address[client_socket] = client_address
                # Send hello to all connected client
                hello = "[+] User {} has connected from {}\n".format(socket_to_username[client_socket], socket_to_address[client_socket])
                print(hello)
                broadcast(server_socket, client_socket, hello)
            # If there is another socket in INPUTS, then there is message has arrived and it is readable,
            # so read (receive) it and send it as broadcast message to all connected clients
            else:
                try:
                    data = s.recv(BUFFER)
                    # If there is something received, then send it as broadcast message
                    if data:
                        if MONITOR == True:
                            print(data.decode())
                        if data.decode() == "[" + socket_to_username[s] + "]: " + "quit\n":
                            s.close()
                            if s in INPUTS:
                                INPUTS.remove(s)
                            OUTPUTS.remove(s)
                            goodbye = "[-] User {} has disconnected from {}\n".format(socket_to_username[s], socket_to_address[s])
                            print(goodbye)
                            broadcast(server_socket, s, goodbye)
                            del socket_to_username[s]
                            del socket_to_address[s]
                        elif data.decode() == "[" + socket_to_username[s] + "]: " + "user\n":
                            send_user_list(s, socket_to_username)
                        else:
                            broadcast(server_socket, s, data.decode())
                    # If not data, the connection is broken, remove a socket of the connection from lists
                    # and notify information about offline client to all other clients
                    else:
                        if s in INPUTS:
                            INPUTS.remove(s)
                        OUTPUTS.remove(s)
                        goodbye = "[-] User {} has disconnected from {}\n".format(socket_to_username[s], socket_to_address[s])
                        print(goodbye)
                        broadcast(server_socket, s, goodbye)
                        del socket_to_username[s]
                        del socket_to_address[s]
                except:
                    goodbye = "[-] User {} has disconnected from {}\n".format(socket_to_username[s], socket_to_address[s])
                    print(goodbye)
                    broadcast(server_socket, s, goodbye)
                    del socket_to_username[s]
                    del socket_to_address[s]
                    continue

    server_socket.close()

# Function to send broadcast messages to all connected client, excetp sender and server itself
def broadcast(server_socket, s, message):
    for sock in INPUTS:
        if sock != server_socket and sock != s:
            try:
                sock.send(message.encode())
            except:
                # Broken socket connection
                sock.close()
                # Remove it
                if sock in INPUTS:
                    INPUTS.remove(sock)
def send_user_list(s, socket_to_username):
    user_list = []
    number_of_users = 0
    for sock in socket_to_username.keys():
        if sock is s:
            user_list.append("[" + socket_to_username[sock] + "]")
            number_of_users += 1
        else:
            user_list.append(socket_to_username[sock])
            number_of_users += 1
    user_list_string = "# {} online user(s) in this chat room: ".format(number_of_users) + ", ".join(user_list) + "\n"
    s.send(user_list_string.encode())

if __name__ == "__main__":
    sys.exit(chat_server())

