from threading import Thread
import socket
from .logging import Logger
from .commandhandler import CommandHandler
from templates import template # I dont know why this works, apparently, the import its made from the dir of 'server.py'
from json import loads, dumps, JSONDecodeError


class Handler:
    def __init__(self, server: socket.socket, user_limit: int = 64, bufsize: int = 4096, logfile=None, name_length: str=30):
        self.server = server
        self.user_limit = user_limit
        self.database = {}
        self.last_id = 0
        self.bufsize = bufsize
        self.logger = Logger(logfile=logfile)
        self.command_handler = CommandHandler(self)
        self.name_length = name_length

    def add_client(self, client_obj: socket.socket) -> int:
        # Add a client to the client list

        # Pick an Id for the new client
        self.database[self.last_id + 1] = {"socket": client_obj, "name": self.last_id + 1}
        self.last_id += 1

        # Start dedicated thread for the client
        self.database[self.last_id]["thread"] = Thread(target=self._dedicated_client_handler, args=[self.last_id],
                                                       daemon=False)
        self.database[self.last_id]["thread"].start()
        self.broadcast_message(template.server_message(f"User with id {self.last_id} joined the server."))
        self.logger.log_msg("SERVER", f"User with id {self.last_id} joined the server.")
        return self.last_id

    def broadcast_message(self, message) -> None:
        for client in self.database:
            self.send_message(client, message)

    def send_message(self, client_id: int, message: str) -> None:
        try:
            self.database[client_id]["socket"].send(message.encode("utf-8"))

        except Exception as e:
            self.logger.log_msg("error",
                                f"An error has occurred when trying to send a message to {client_id}, and the error was ->{e}<-")

    def disconnect_client(self, client_id):
        # Disconnects a client in a secure way
        if client_id not in self.database:
            raise ValueError(f"Client not found: {client_id}")

        else:
            # Get the name of the client
            client_name = self.database[client_id]["name"]
            # Close thread (Im going to assume that it will stop)

            # Remove the client from the database
            self.database[client_id]["socket"].close()
            del self.database[client_id]
            self.broadcast_message(template.server_message(f"'{client_name}#{client_id}' left the server."))

    def _dedicated_client_handler(self, client_id) -> None:
        # Handles the connection between a client and the server.

        while client_id in self.database:
            try:
                msg = self.database[client_id]["socket"].recv(self.bufsize)

            except ConnectionAbortedError:
                self.logger.log_msg("log", f"User with id {client_id} has disconnected")

                if client_id in self.database:  # Disconnect in case that the
                    self.disconnect_client(client_id)

                break

            except:
                if client_id in self.database:
                    self.logger.log_msg("error", f"Client {client_id} has been disconnected, or some error ocurred.")
                    self.disconnect_client(client_id)   # TODO Fix this mess and avoid triggering errors when disconnected.
                    
                else:
                    break
                return

            self._handle_client_input(client_id, msg)

    def _handle_client_input(self, client_id:int, client_input:str) -> None:
        # Behaves according to the input of the client towards the server
        try:
            client_input = loads(client_input)

        except JSONDecodeError:
            self.logger.log_msg("error", f"Client with id '{client_id}' has sent an invalid message. ('{client_input}')")

        if client_input["type"] == "message":  # Default message
            self.broadcast_message(template.common_message(client_id, self.database[client_id]["name"], client_input["message"]))
            self.logger.log_msg(f"Message from {self.database[client_id]['name']}#{client_id}", client_input["message"])

        elif client_input["type"] == "command":
            self.logger.log_msg("log", f"User '{self.database[client_id]['name']}#{client_id}' has issued with command '{client_input['command']}'")
            self.command_handler.execute_command(client_id, client_input["command"], client_input["pars"])


        else:
            self.logger.log_msg("warning", f"Client with id {client_id} sent an unknown type of message: '{client_input['type']}'")


