from json import dumps


def common_client_message(message:str) -> str:
    # Message that the client sends to the server
    return dumps({"type": "msg", "message": message})


def common_message(author_id:int, author_name:str, message:str) -> str:
    # Message that the client receives
    return dumps({"type": "msg", "author_id": author_id, "author_name": author_name, "msg": message})


def server_message(message:str) -> str:
    return dumps({"type": "server", "msg": message})


def direct_message(author_id: int, author_name: str, message: str) -> str:
    return dumps({"type": "direct_message", "author_name": author_name, "author_id": author_id, "message": message})


def command_message(command: str, parameters: list):
    return dumps({"type": "command", "command": command, "pars": parameters})


def command_result(code: int) -> str:
    # Format of message that contains the code about a command used. (Used by the server and received by the client)
    return dumps({"type":"result", "code":code})


def register(name: str, passwd: str) -> str:
    # Message sent from the client to the server in order to create account
    return dumps({"type": "register", "name": name, "passwd": passwd})


def login(name: str, passwd: str) -> str:
    # Message sent from the client to the server in order to login into an existing account
    return dumps({"type": "login", "name": name, "passwd": passwd})

# TODO Keep adding new types of messages


