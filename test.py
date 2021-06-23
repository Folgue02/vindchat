import socket
from threading import Thread
from templates import template
from client.syntax import parse_syntax

address = "localhost"
port = 25565

me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def sender():
    while True:
        userinput = input(">")

        # In case it is a command
        if userinput.startswith("/"):
            # Nothing specified
            if userinput[1:] == "":
                continue
        
            else:
                parsed = parse_syntax(userinput[1:])
                command = parsed[0]
                parameters = parsed[1:] if len(parsed) > 1 else []
                print("Sending command" + template.command_message(command, parameters))
                me.send(template.command_message(command, parameters).encode("utf-8"))


        else:
            me.send(template.common_client_message(userinput).encode("utf-8"))


try:
    me.connect((address, port))
    Thread(target=sender, daemon=False).start()
    while True:
        msg = me.recv(1028)
        print(msg.decode("utf-8"))

except Exception as e:
    print(e, type(e))
    exit()
