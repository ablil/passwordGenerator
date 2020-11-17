import os
import pickle
from datetime import datetime
from typing import Dict, List


class Cache:
    def __init__(self):
        self.path = os.path.join(os.path.expanduser("~"), ".qpg/")
        self.filename = "passwords.pickle"
        self.abs_filename = os.path.join(self.path, self.filename)

        self.saved_passwords: List[Dict] = list()

        # mkdir cache path
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        # read cache file
        if os.path.exists(self.abs_filename):
            with open(self.abs_filename, "rb") as pickleData:
                self.saved_passwords = pickle.load(pickleData)

    def save(self, password: str, generated=None):
        """save password"""
        if not generated:
            generated = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")

        self.saved_passwords.append({"generated": generated, "password": password})

        with open(self.abs_filename, "wb") as data:
            pickle.dump(self.saved_passwords, data)

    def list(self, n=-1):
        """get saved passwords"""

        with open(self.abs_filename, "rb") as data:
            self.saved_passwords = pickle.load(data)

        return self.saved_passwords

    def clear(self):
        """clear saved passwords"""
        self.saved_passwords = list()
        if os.path.exists(self.abs_filename):
            os.remove(self.abs_filename)