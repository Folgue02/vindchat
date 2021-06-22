import socket
from threading import Thread
from templates import template

address = "localhost"
port = 25565


def sender():
    while True:
        userinput = input(">")

        # In case it is a command
        if userinput.startswith("/"):

        me.send(template.common_client_message(userinput).encode("utf-8"))


me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    me.connect((address, port))
    Thread(target=sender, daemon=False).start()
    while True:
        msg = me.recv(1028)
        print(msg.decode("utf-8"))

except Exception as e:
    print(e, type(e))
    exit()
