import socket
from threading import Thread
from templates import template
from client.syntax import parse_syntax
from json import loads, JSONDecodeError
from share.logging import Logger
from traceback import print_exc

address = "localhost"
port = 25565

me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logger = Logger()

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
        msg = me.recv(1028).decode("utf-8")

        try:
            msg = loads(msg)

        except JSONDecodeError:
            logger.log_msg("error", "Cannot decode message sent by the server.")

        if msg["type"] == "msg":
            logger.log_msg(f"Message from {msg['author_name']}#{msg['author_id']}", msg["msg"])

        elif msg["type"] == "server":
            logger.log_msg("SERVER", msg["msg"])
        else:
            print(msg)

except Exception as e:
    print_exc()
    exit()
