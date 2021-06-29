from share.logging import Logger
from templates import template

class ProtocolHandler:
    def __init__(self, server):
        self.server = server
        self.protocols = {"msg": self._msg, "command": self._command}


    def execute_input(self, session_id: int, client_input: dict):
        """
        Takes action based on the input of the client specified.
        """

        if not "type" in  client_input:
            self.server.logger.log_msg("error", f"execute_input: Session with id '{session_id}' has sent an invalid message. (doesn't contain key 'type')")
            self.server.disconnect_client(session_id)

        elif not client_input["type"] in self.protocols:
            self.server.logger.log_msg("warning", f"Session with id '{session_id}' has sent an unknown type of message: '{client_input['type']}'")

        else:
            self.protocols[client_input['type']](session_id, client_input)

    def _msg(self, session_id: int, client_input):
        
        # Trim the message
        client_input["message"] = client_input["message"].strip()

        # In case that the message its empty
        if client_input["message"] == "":
            pass

        else:
            self.server.logger.log_msg(f"{self.server.get_session_name(session_id)}#{session_id}", client_input["message"])
            self.server.broadcast_message(template.common_message(session_id, self.server.get_session_name(session_id), client_input["message"]))



    def _command(self, session_id: int, client_input: dict):
        self.server.logger.log_msg("log", f"User '{self.server.get_session_name(session_id)}#{session_id}' has issued with command '{client_input['command']}'")
        self.server.command_handler.execute_command(session_id, client_input["command"], client_input["pars"])


