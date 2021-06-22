from json import dumps


def common_client_message(message:str) -> str:
    # Message that the client sends to the server
    return dumps({"type": "message", "message": message})


def common_message(author_id:int, author_name:str, message:str) -> str:
    # Message that the client receives
    return dumps({"type": "message", "author_id": author_id, "author_name": author_name, "msg": message})


def server_message(message:str) -> str:
    return dumps({"type": "server", "msg": message})


def direct_message(author_id:int, author_name:str, message:str) -> str:
    return dumps({"type": "direct_message", "author_name": author_name, "author_id": author_id, "message": message})


def command_message(command: str, parameters: list):
    return dumps({"type": "command", "command": command, "pars": parameters})


def command_result(code: int) -> str:
    # Format of message that contains the code about a command used. (Used by the server and received by the client)
    return dumps({"type":"result", "code":code})

# TODO Keep adding new types of messages


