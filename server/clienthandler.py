from threading import Thread
import socket
from share.logging import Logger
from .commandhandler import CommandHandler
from .accounthandler import AccountHandler
from templates import template # I dont know why this works, apparently, the import its made from the dir of 'server.py'
from json import loads, JSONDecodeError


class Handler:
    def __init__(self, server: socket.socket, database_file: str, user_limit: int = 64, bufsize: int = 4096, logfile=None, name_length: str=30):
        self.server = server
        self.user_limit = user_limit
        self.sessions = {}
        self.last_id = 0
        self.bufsize = bufsize
        self.logger = Logger(logfile=logfile)
        self.database = AccountHandler(database_file)
        self.command_handler = CommandHandler(self)
        self.name_length = name_length

    def add_client(self, client_obj: socket.socket) -> int:
        # Add a client to the client list

        # Pick an Id for the new client
        self.sessions[self.last_id + 1] = {"socket": client_obj, "name": self.last_id + 1}
        self.last_id += 1

        # Start dedicated thread for the client
        self.sessions[self.last_id]["thread"] = Thread(target=self._dedicated_client_handler, args=[self.last_id],
                                                       daemon=False)
        self.sessions[self.last_id]["thread"].start()
        self.broadcast_message(template.server_message(f"User with id {self.last_id} joined the server."))
        self.logger.log_msg("SERVER", f"User with id {self.last_id} joined the server.")
        return self.last_id

    def broadcast_message(self, message) -> None:
        for client in self.sessions:
            self.send_message(client, message)

    def send_message(self, client_id: int, message: str or bytes) -> None:
        """
        Send a message to a client
        :param client_id:
        :param message:
        :return:
        """

        if isinstance(message, str):
            message = message.encode("utf-8")

        # The client doesn't exist
        if not client_id in self.sessions:
            raise KeyError(f"Client '{client_id}' doesn't exist.")

        try:

            self.sessions[client_id]["socket"].send(message.encode("utf-8"))

        except Exception as e:
            self.logger.log_msg("error",
                                f"An error has occurred when trying to send a message to {client_id}, and the error was '{e}'")
            self.disconnect_client(client_id)

    def disconnect_client(self, client_id):
        # Disconnects a client in a secure way
        if client_id not in self.sessions:
            raise ValueError(f"Client not found: {client_id}")

        else:
            # Get the name of the client
            client_name = self.sessions[client_id]["name"]
            # Close thread (Im going to assume that it will stop)

            # Remove the client from the database
            self.sessions[client_id]["socket"].close()
            del self.sessions[client_id]
            self.broadcast_message(template.server_message(f"'{client_name}#{client_id}' left the server."))

    def _dedicated_client_handler(self, client_id) -> None:
        """
        Handles the connection of the client
        :param client_id:
        :return:
        """
        # Wait for register or login as first message, if its not the client will be disconnected.
        msg = self.sessions[client_id]["socket"].recv(self.bufsize)

        try:
            first_msg = loads(msg.decode("utf-8"))

        except UnicodeError:
            self.logger.log_msg("error", f"Package from '{client_id}' couldn't be decoded.")
            self.disconnect_client(client_id)
            return

        except JSONDecodeError:
            self.logger.log_msg("error", f"Package from '{client_id}' couldn't be turned into a dictionary.")
            self.disconnect_client(client_id)
            return

        except:
            self.logger.log_msg("error", f"Unknown exception while awaiting for login/register from client '{client_id}'")
            self.disconnect_client(client_id)
            return

        # First msg its not a login or register package
        if not first_msg["type"] == "login" and not first_msg["type"] == "register":
            self.logger.log_msg("error", f"Client '{client_id}' didn't send a login/register package.")
            self.disconnect_client(client_id)
            return

        else:
            if first_msg["type"] == "login":
                if self.database.verify_login(first_msg["name"], first_msg["passwd"]):
                    self.sessions[client_id]["name"] = first_msg["msg"] # Change name of the session to the account name

                else:
                    self.logger.log_msg("log", f"Client '{client_id}' failed login into acc '{first_msg['name']}', disconnecting him...")
                    self.disconnect_client(client_id)
                    return

            elif first_msg["type"] == "register":
                if self.database.register_account(first_msg["name"], first_msg["passwd"]):  # account register went well
                    self.logger.log_msg("log", f"Account registered as '{first_msg['name']}'")
                    self.sessions[client_id]["socket"].send(template.command_result(0).encode("utf-8"))
                    self.disconnect_client(client_id)
                    return

                else:  # Something went wrong during account registration
                    self.sessions[client_id]["socket"].send(template.command_result(6).encode("utf-8"))
                    self.disconnect_client(client_id)
                    return

        while client_id in self.sessions:
            try:
                msg = self.sessions[client_id]["socket"].recv(self.bufsize)

            except ConnectionAbortedError:
                self.logger.log_msg("log", f"User with id {client_id} has disconnected")

                if client_id in self.sessions:  # Disconnect in case that the
                    self.disconnect_client(client_id)

                break

            except:
                if client_id in self.sessions:
                    self.logger.log_msg("error", f"Client {client_id} has been disconnected, or some error ocurred.")
                    self.disconnect_client(client_id)   # TODO Fix this mess and avoid triggering errors when disconnected.
                    
                else:
                    break
                return

            self._handle_client_input(client_id, msg)

    def _handle_client_input(self, client_id: int, client_input: str) -> None:
        # Behaves according to the input of the client towards the server
        try:
            client_input = loads(client_input)

        except JSONDecodeError:
            self.logger.log_msg("error", f"Client with id '{client_id}' has sent an invalid message. ('{client_input}')")

        if client_input["type"] == "msg":  # Default message TODO FIX THIS
            self.broadcast_message(template.common_message(client_id, self.sessions[client_id]["name"], client_input["message"]))
            self.logger.log_msg(f"Message from {self.sessions[client_id]['name']}#{client_id}", client_input["message"])

        elif client_input["type"] == "command":
            self.logger.log_msg("log", f"User '{self.sessions[client_id]['name']}#{client_id}' has issued with command '{client_input['command']}'")
            self.command_handler.execute_command(client_id, client_input["command"], client_input["pars"])

        else:
            self.logger.log_msg("warning", f"Client with id {client_id} sent an unknown type of message: '{client_input['type']}'")


