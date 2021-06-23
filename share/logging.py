from datetime import date, datetime
import os


class Logger:
    def __init__(self, logfile=None):
        self.logfile = logfile

    def log_msg(self, msg_type: str, message: str) -> None:
        string = f"[{datetime.now().strftime('%H:%M:%S')} // {msg_type}]: {message}"

        if self.logfile != None:
            if not os.path.exists(self.logfile):
                open(self.logfile, "w").write(string)
            
            else:  # If logfile exists
                old_content = open(self.logfile, "r").read()
                open(self.logfile, "w").write(old_content + "\n" + string)

        print(string) 

