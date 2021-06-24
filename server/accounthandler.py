import os
from json import loads, dumps, JSONDecodeError

class AccountHandler:
    def __init__(self, server, database_file):  # TODO Rework this to use sqlite
        self.database_file = database_file
        self.server = server

        if not os.path.isfile(database_file):
            raise FileNotFoundError(f"Database file doesn't exist. ('{self.database_file}')")

    def _write_database(self, new_content: str):
        open(self.database_file, "w").write(new_content)

    def _read_database(self) -> str:
        return open(self.database_file, "r").read()

    def get_account(self, account_name: str) -> dict:
        database = loads(self._read_database())

        if not account_name in database:
            raise KeyError(f"get_account: Cannot find account with name {account_name}")

        else:
            return database[account_name]

    def modify_account(self, account_name: str, name: str=None, passwd: str=None, nick: str=None):
        # Modifies an account and saves the changes to the database in the drive
        old_content = loads(self._read_database())

        if not account_name in old_content:
            raise KeyError(f"modify_account: Account with name '{account_name}' couldn't be found.")

        else:
            new_account = {"name": name, "nick": nick, "passwd": passwd}
            old_account = old_content[account_name]

            # Merge accounts
            for key in old_account:
                if new_account[key]:
                    old_account[key] = new_account[key]

                else:
                    pass

            # NOTE: old_content and old_account end up being the new ones.
            old_content[account_name] = old_account
            self._write_database(dumps(old_content))

    def remove_account(self, account_name: str):
        # Removes an account and saves the changes to the database in the drive

        old_content = loads(self._read_database())

        if not account_name in old_content:
            raise KeyError(f"Account with name '{account_name}' couldn't be found.")

        else:
            del old_content[account_name]
            self._write_database(dumps(old_content))


    def register_account(self, name: str, passwd: str) -> bool: # TODO Encrypt passwords in some way?
        # Creates account, in case that the account already exists it will raise a KeyError

        accounts = loads(self._read_database())
        if name in accounts: # TODO Use the name length max?
            return False

        else:
            accounts[name] = {"passwd": passwd, "nick":name}
            self._write_database(dumps(accounts))
            return True


    def verify_login(self, name:str, passwd:str) -> bool:
        # Checks if the login credentials are valid, returns a bool representing its validity
        accounts = loads(self._read_database())

        if not name in accounts:
            return False

        else:
            if accounts[name]["passwd"] != passwd:
                return False

            else:
                return True
