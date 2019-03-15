import socket, select, sys, os
from color  import *

INPUTS = []
OUTPUTS = []
ERRORS = []
BUFFER = 8192
# CURSOR_UP = "\033[F"
# CLEAR_LINE = "\033[K"
WIDTH = os.get_terminal_size().columns

def chat_client():
    if (len(sys.argv) != 4):
        print("\033[91m" + "# Usage: python3.7 chat_client.py $HOST $PORT $USER" + "\033[0m")
        sys.exit()
    # Parse command line arguments
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    username = sys.argv[3]
    # Create socket on client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)
    # Connect to the server
    try:
        client_socket.connect((HOST, PORT))
    except:
        print(fg.RED, "# Unable to connect.", fg.RED)
        sys.exit()
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
    print('# Connected to VERA server. Send "user" to see who is online, send "quit" to exit.\n')
    # Send username to server
    client_socket.send(username.encode())
    while True:
        INPUTS = [sys.stdin, client_socket]
        readable, writable, exceptional = select.select(INPUTS, OUTPUTS, ERRORS)
        # There is incoming message from remote server
        for s in readable:
            if s is client_socket:
                data = s.recv(BUFFER)
                if not data:
                    print("# Disconnected from VERA server.")
                    sys.exit()
                else:
                    sys.stdout.write(data.decode())
            # If user entered a message
            else:
                user_input = sys.stdin.readline()
                if user_input == "quit\n":
                    print("# The VERA program aborted by user. Exiting...")
                    s.close()
                    sys.exit()
                else:
                    message = "[" + username + "]: " + user_input
                    client_socket.send(message.encode())

if __name__ == "__main__":
    sys.exit(chat_client())