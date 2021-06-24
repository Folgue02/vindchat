import socket
from threading import Thread
from templates import template
from client.syntax import parse_syntax
from json import loads, JSONDecodeError
from share.logging import Logger
from traceback import print_exc
from share import codes
from argparse import ArgumentParser

address = "localhost"
port = 25565

me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logger = Logger()

ACCOUNT_NAME = "guest"
ACCOUNT_PASSWD = "guest"

args = ArgumentParser()

args.add_argument("action", default=None, help="[register/login]")
args.add_argument("name", default=None, help="Username")
args.add_argument("passwd", default=None, help="Password")
ARGS = args.parse_args()

def sender():

    # Set credentials
    if ARGS.name:
        account_name = ARGS.name

    if ARGS.passwd:
        account_passwd = ARGS.passwd

    # Register / Login
    if ARGS.action == "register":
        me.send(template.register(account_name, account_passwd).encode("utf-8"))

    elif ARGS.action == "login":
        me.send(template.login(account_name, account_passwd).encode("utf-8"))

    else:
        me.send(template.login(account_name, account_passwd).encode("utf-8"))

    while True:
        try:
            userinput = input(">")
        except KeyboardInterrupt:
            me.close()
            exit(0)

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
            me.close()
            exit(0)

        if msg["type"] == "msg":
            logger.log_msg(f"Message from {msg['author_name']}#{msg['author_id']}", msg["msg"])

        elif msg["type"] == "server":
            logger.log_msg("SERVER", msg["msg"])

        elif msg["type"] == "result":
            logger.log_msg("server_feedback", f"{msg['code']} - {codes.CODES[msg['code']]}")

        else:
            print(msg)

except Exception:
    print_exc()
    exit()
