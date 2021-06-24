import socket
from threading import Thread
from traceback import print_exc

# Project libraries
from server.clienthandler import Handler
from templates import template

# Configuration
ADDRESS = "localhost"
PORT = 25565
BUFSIZE = 4096

# Socket object of the server
SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOC.bind((ADDRESS, PORT))

# Client handler
HANDLER = Handler(SOC, "./database.json",bufsize=BUFSIZE, logfile="./logs.txt")


def listener():
    while True:
        c, a = SOC.accept()
        
        print(c, a)

        # Add to the handler
        new_client = HANDLER.add_client(c)
        print(f"New client added to the handler: {new_client}")


def main():
    SOC.listen(5)
    LISTENER_THREAD.start()

    while True:
        userinput = input(f"({ADDRESS}:{PORT})>>>")

        # Execute input 
        try:
            exec(userinput)

            # Ignore if input its empty
            if userinput == "":
                continue

        except KeyboardInterrupt: # TODO Make it work
            print("Closing socket...")
            SOC.close()
            print("Socket closed, closing server script...")
            exit(0)

        except Exception:
            print_exc()


if __name__ == "__main__":
    
    LISTENER_THREAD = Thread(target=listener, daemon=True)

    main()
