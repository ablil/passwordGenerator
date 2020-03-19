import os
import pickle
from datetime import datetime

class Cache:
    def __init__(self):
        self.cachePath = os.path.join(os.path.expanduser("~"), ".passwordGenerator/")
        self.cacheFilename = "passwords.pickle"
        self.cacheAbsoluteFilename = os.path.join(self.cachePath, self.cacheFilename)
        self.cacheSize = 10
        self.passwords = list()

        if not os.path.exists(self.cachePath):
            os.mkdir(self.cachePath)

        if not os.path.exists(self.cacheAbsoluteFilename):
            # create file
            with open(os.path.join(self.cachePath, self.cacheFilename), "wb") as file:
                pass
        else:
            try:
                with open(self.cacheAbsoluteFilename, "rb") as pickleData:
                    self.passwords = pickle.load(pickleData)
            except EOFError:
                pass

    def storePassword(self, password: str):
        self.passwords.append((Cache.getCurrentTime(), password))

        if len(self.passwords) > self.cacheSize:
            self.passwords.pop(0)

        with open(os.path.join(self.cachePath, self.cacheFilename), "wb") as pickleData:
            pickle.dump(self.passwords, pickleData)

    def getRecentPasswords(self, n: int):
        assert os.path.exists(os.path.join(self.cachePath, self.cacheFilename))

        with open(self.cacheAbsoluteFilename, "rb") as pickleData:
            try:
                self.passwords = pickle.load(pickleData)
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

    def emptyCache(self):
        self.passwords = list()
        if os.path.exists(self.cacheAbsoluteFilename):
            os.remove(self.cacheAbsoluteFilename)


if __name__ == "__main__":
    print("This is just the cache handler")
