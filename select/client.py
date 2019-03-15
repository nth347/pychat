import socket, select, sys

CURSOR_UP = "\033[F"
CLEAR_LINE = "\033[K"

print("   ____   ____                      \n"
      "   \   \ /   / ____ _______ _____   \n"
      "    \   Y   /_/ __ \\\_  __ \\\__  \  \n"
      "     \     / \  ___/ |  | \/ / __ \_\n"
      "      \___/   \___  >|__|   (____  /\n"
      "                  \/             \/ \n"
      "VERA v1.0 | March 2019 | NTH347 | Passion is power.\n")

def chat_client():
    if (len(sys.argv) < 4):
        print("# Usage: python3.7 chat_client.py $HOST $PORT $USER")
        sys.exit()
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    USER = sys.argv[3]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)
    try:
        client_socket.connect((HOST, PORT))
    except:
        print("\033[91m" + "# Unable to connect!" +"\033[0m")
        sys.exit()
    print("# Connected to remote server!\n")
    # sys.stdout.write("[Me]: "); sys.stdout.flush()
    while True:
        INPUTS = [sys.stdin, client_socket]
        # Get the list sockets which are readable
        readable, writable, in_error = select.select(INPUTS, [], [])
        for s in readable:
            if s == client_socket:
                # Incoming message from remote server
                data = s.recv(4096)
                if not data:
                    print("\033[91m" + "# Disconnected from chat server!" + "\033[0m")
                    sys.exit()
                if data:
                    # Print data
                    # sys.stdout.write(LINE_UP)
                    # sys.stdout.write(CLEAR_LINE)
                    sys.stdout.write(data.decode());
                    # sys.stdout.write("[Me]: "); sys.stdout.flush()
            else:
                # User entered a message
                user_input = sys.stdin.readline()
                if user_input == "":
                    print(CLEAR_LINE)
                else:
                    msg = "[" + USER + "]: " + user_input
                    client_socket.send(msg.encode())
                # sys.stdout.write("[Me]: "); sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(chat_client())
