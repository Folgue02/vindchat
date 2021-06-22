from termcolor import colored
from colorama import init
from datetime import date, datetime
import os
init()


class Logger:
    def __init__(self, logfile=None):
        self.logfile = logfile

    def log_msg(self, msg_type:str, message:str) -> None:
        string = f"[{date.today().isoformat()} // {msg_type}]: {message}"

        if self.logfile != None: # TODO Fix this mess
            if not os.path.exists(self.logfile):
                open(self.logfile, "w").write(string)
            
            else:  # If logfile exists
                open(self.logfile, "w").write(open(self.logfile, "r").read() + "\n" + string)

        print(string) # ADD COLORS TO THE TERMINAL

