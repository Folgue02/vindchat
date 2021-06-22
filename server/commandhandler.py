from .clienthandler import Handler
from logging import Logger
from traceback import print_exc

class CommandHandler:
    def __init__(self, server:Handler):
        self.server = server
        self.commands = {}

    def execute_command(self, author_id, command:str, parameters:list) -> int:
        # Executes a command and returns a boolean value that represents the result of the command execution.
        if not command in self.commands:
            print("Command not found") #  TODO Return a value or raise an exception

        else:
            try:
                self.commands[command](author_id, parameters)
            except Exception as e:
                print_exc() #  TODO Return a message to the author ?

    def name(self, author_id, parameters):
        if len(parameters) == 0:
            raise ValueError(f"No parameters specified by the client.")

        # TODO Stablish a limit of characters in a name

        self.server.database[author_id]["name"] = parameters[0]


