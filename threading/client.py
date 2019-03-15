import socket
import threading
import sys


HOST = "localhost"
PORT = 8888
BUFFER = 2048
ADDRESS = (HOST, PORT)
name = sys.argv[1]
# password = sys.argv[2]


# Function to handle user input
def handle_input(client_socket):
    # Send username to server
    client_socket.send(name.encode())
    # Send password to server
    # client_socket.send(password.encode())
    # While loop to wait user input
    while True:
        out_message = input()
        if out_message == "quit":
            print("# The program aborted by user command. Exiting...")
            client_socket.send("quit".encode())
            client_socket.close()
            sys.exit()
        else:
            client_socket.send(out_message.encode())


# Function to recieve messages from the server and display them
def handle_output(client_socket):
    # While loop to recieve messages from server
    while True:
        try:
            in_message = client_socket.recv(BUFFER).decode()
            print(in_message)
        except:
            client_socket.close()
            break


if __name__ == "__main__":
    # Print banner of the application
    print(""
          "   ____   ____                      \n"
          "   \   \ /   / ____ _______ _____   \n"
          "    \   Y   /_/ __ \\\_  __ \\\__  \  \n"
          "     \     / \  ___/ |  | \/ / __ \_\n"
          "      \___/   \___  >|__|   (____  /\n"
          "                  \/             \/ \n"
          'VERAv1.0 | March 2019 | NTH347 | "Passion is power."\n')
    try:
        # Create client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server via address
        client_socket.connect(ADDRESS)
        print("# Connected to {}:{}".format(HOST, PORT))
        threading.Thread(target=handle_input, args=(client_socket,)).start()
        threading.Thread(target=handle_output, args=(client_socket,)).start()
    except KeyboardInterrupt:
        print("The program aborted by CTRL + C.")
        client_socket.send("quit".encode())
        client_socket.close()
        sys.exit()
