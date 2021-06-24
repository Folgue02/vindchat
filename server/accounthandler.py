import os
from json import loads, dumps, JSONDecodeError


class AccountHandler:
    def __init__(self, database_file):  # TODO Rework this to use sqlite
        self.database_file = database_file
        if not os.path.isfile(database_file):
            raise FileNotFoundError(f"Database file doesn't exist. ('{self.database_file}')")

    def _write_database(self, new_content: dict or str):
        if new_content.is_instance(str):
            new_content = dumps(new_content)

        open(self.database_file, "w").write(new_content)

    def _read_database(self) -> str:
        return open(self.database, "r").read()

    def register_account(self, name:str, passwd:str): # TODO Encrypt passwords in some way?
        # Creates account, in case that the account already exists it will raise a KeyError

        accounts = loads(self._read_database())
        if name in accounts: # TODO Use the name length max?
            raise KeyError(f"There is already an account with name '{name}'.")

        else:
            accounts[name] = {"passwd": passwd}

    def verify_login(self, name:str, passwd:str) -> bool:
        # Checks if the login credentials are valid, returns a bool representing its validity
        accounts = self._read_database()

        if not name in accounts:
            return False

        else:
            if accounts[name]["passwd"] != passwd:
                return False

            else:
                return True
