import os
import pickle
from datetime import datetime

class Cache:
    def __init__(self):
        self.path = os.path.join(os.path.expanduser("~"), ".qpg/")
        self.filename = "passwords.pickle"
        self.abs_filename = os.path.join(self.path, self.filename)

        self.cacheSize = 10
        self.passwords = list()

        # mkdir cache path
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        # create cache file
        if not os.path.exists(self.abs_filename):
            with open(os.path.join(self.path, self.filename), "wb") as file:
                pass
        else:
            try:
                with open(self.abs_filename, "rb") as pickleData:
                    self.passwords = pickle.load(pickleData)
            except EOFError:
                pass

    def save(self, password: str):
        """save password"""
        self.passwords.append((Cache.getCurrentTime(), password))

        with open(os.path.join(self.path, self.filename), "wb") as data:
            pickle.dump(self.passwords, data)

    def list(self, n: int):
        """get saved passwords"""

        with open(self.abs_filename, "rb") as data:
            try:
                self.passwords = pickle.load(data)
            except EOFError:
                return list()

        return (
            self.passwords[-1 : -n - 1 : -1]
            if n < len(self.passwords)
            else self.passwords
        )

    @staticmethod
    def getCurrentTime():
        now = datetime.now()
        return now.strftime('%Y:%m:%d-%H:%M:%S')

    def clear(self):
        """clear saved passwords"""
        self.passwords = list()
        if os.path.exists(self.abs_filename):
            os.remove(self.abs_filename)
