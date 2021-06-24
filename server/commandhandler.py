from traceback import print_exc
from templates import template
from share.codes import CODES


class CommandHandler:
    def __init__(self, server):
        self.server = server
        self.commands = {"chnick": self.chnick}

    def execute_command(self, author_id, command: str, parameters: list) -> int:
        # Executes a command and returns a boolean value that represents the result of the command execution.
        if not command in self.commands:
            self.server.sessions[author_id]["socket"].send(template.command_result(2).encode("utf-8"))

        else:
            try:
                self.commands[command](author_id, parameters)
            except Exception as e:
                self.server.sessions[author_id]["socket"].send(template.command_result(1).encode("utf-8"))

    def chnick(self, author_id, parameters):
        if len(parameters) == 0:
            self.server.sessions[author_id]["socket"].send(template.command_result(3).encode("utf-8"))

        elif len(parameters[0]) > self.server.name_length:
            self.server.sessions[author_id]["socket"].send(template.command_result(5).encode("utf-8"))

        else:
            self.server.sessions[author_id]["name"] = parameters[0]
            
            # Change nick in the database
            try:
                self.server.database.modify_account(self.server.get_session_account(author_id), nick=parameters[0])
            except Exception as e:
                self.server.logger.log_msg("error", f"chnick: Couldn't save changes to the database: '{e}'")
            



# TODO Write more builtin commands
