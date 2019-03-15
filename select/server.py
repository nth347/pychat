import socket, select, sys

HOST = "localhost"
PORT = 9999
BUFFER = 4096
INPUTS = []
OUTPUTS = []
ERRORS = []
# CURSOR_UP = "\x1b[1A"
# CLEAR_LINE = "\x1b[2K"

print("   ____   ____                      \n"
      "   \   \ /   / ____ _______ _____   \n"
      "    \   Y   /_/ __ \\\_  __ \\\__  \  \n"
      "     \     / \  ___/ |  | \/ / __ \_\n"
      "      \___/   \___  >|__|   (____  /\n"
      "                  \/             \/ \n"
      "VERA v1.0 | March 2019 | NTH347 | Passion is power.\n")

def chat_server():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable re-use address feature on the socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to address and listen for connection requests
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    # Add server socket object to the list of readable connection
    INPUTS.append(server_socket)    # INPUTS = [server_socket]
    print("VERA server running on {}:{}".format(HOST, PORT))
    while True:
        readable, writable, exceptional = select.select(INPUTS, OUTPUTS, ERRORS, 0)
        for s in readable:
            # If there is the server socket in INPUTS, it means that a new client has arrived,
            # therefore, it calls accept() and adds a returned socket to INPUTS
            if s is server_socket:  # s == server_socket
                client_socket, address = server_socket.accept()
                INPUTS.append(client_socket)
                print("# New client connected: ", address)
                broadcast(server_socket, client_socket, "# New client connected!\n")
            # If there is another socket in INPUTS, then there is message has arrived and it is readable,
            # so read (receive) it and send it as broadcast message to all connected clients
            else:
                # Process data from the socket
                try:
                    data = s.recv(BUFFER)
                    if data:
                        # If there is something recieved, then send it as broadcast message
                        broadcast(server_socket, s, data.decode())
                    else:
                        # Remove the socket that's broken
                        if s in INPUTS:
                            INPUTS.remove(s)
                        broadcast(server_socket, s, "# Client offline!\n")
                except:
                    broadcast(server_socket, s, "# Client offline!\n")
                    continue
        # for s in writable:
            #try:
        # Finally, if there is an error with a socket, it is closed and removed from lists INPUTS, OUTPUTS
        for s in exceptional:
            print("# Exception condition on ", s.getpeername())
            # Remove error socket form INPUTS
            INPUTS.remove(s)
            # Remove error socket from OUTPUTS
            if s in OUTPUTS:
                OUTPUTS.remove(s)
            # Close error socket on server
            s.close()

    server_socket.close()

# Function to send broadcast messages to all connected client, excetp sender and server itself
def broadcast(server_socket, s, message):
    for socket in INPUTS:
        if socket != server_socket and socket != s:
            try:
                socket.send(message.encode())
            except:
                # broken socket connection
                socket.close()
                # Broken socket, remove it
                if socket in INPUTS:
                    INPUTS.remove(socket)

if __name__ == "__main__":
    sys.exit(chat_server())

