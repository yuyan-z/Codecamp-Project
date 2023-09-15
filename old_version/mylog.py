import datetime
import os

class Log:
    def __init__(self):
        self.logs = []
        self.log_file = 'log.txt'
        self.fields = ['time', 'action']

        self.get_log()

    def get_log(self):
        """
        read log from file
        """
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                self.logs = f.readlines()
        else:
            with open(self.log_file, "w") as f:
                f.write(','.join(self.fields) + '\n')

    def add_log(self, action: str):
        log_str = str(datetime.datetime.now()) + ',' + str(action)
        self.logs.append(log_str)

        with open(self.log_file, 'a') as f:
            f.write(log_str + '\n')
