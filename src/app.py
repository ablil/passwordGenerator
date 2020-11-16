from .cli import CLI
import sys
import random
import enum
import argparse
import os
import pickle
from datetime import datetime

SCRIPT_NAME = sys.argv[0].split(".")[0]
ALPHA = [chr(i) for i in range(97, 123)] + [chr(i).upper() for i in range(97, 123)]
NUMERIC = [str(i) for i in range(10)]
ALPHANUMERIC = ALPHA + NUMERIC
HARD = ["!", "@", "#", "$", "%", "^", "&", "*", "_", "-", ";", ",", "."] + ALPHANUMERIC


class Complexity(enum.Enum):
    ALPHA = 1
    NUMERIC = 2
    ALPHANUMERIC = 3
    HARD = 4

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



class PasswordGenerator:
    def __init__(
        self, complexity: Complexity = Complexity.ALPHANUMERIC, length: int = 15
    ):
        self.complexity = complexity
        self.length = length
        self.password = None

    def generate(self):
        if repr(self.complexity) == repr(Complexity.ALPHA):
            self.password = self._generateAlpha()
            print("generated an alpha passwrod")

        if repr(self.complexity) == repr(Complexity.ALPHANUMERIC):
            self.password = self._generateAlphaNumeric()

        if repr(self.complexity) == repr(Complexity.NUMERIC):
            self.password = self._generateNumeric()

        if repr(self.complexity) == repr(Complexity.HARD):
            self.password = self._generateHard()

        return self.password

    def _generateAlpha(self) -> str:
        password = ""
        for i in range(self.length):
            password += ALPHA[random.randint(0, len(ALPHA) - 1)]
        return password

    def _generateNumeric(self):
        password = ""
        for i in range(self.length):
            password += NUMERIC[random.randint(0, len(NUMERIC) - 1)]
        return password

    def _generateAlphaNumeric(self):
        password = ""
        for i in range(self.length):
            password += ALPHANUMERIC[random.randint(0, len(ALPHANUMERIC) - 1)]
        return password

    def _generateHard(self):
        password = ""
        for i in range(self.length):
            password += HARD[random.randint(0, len(HARD) - 1)]
        return password

    def __repr__(self):
        if self.password:
            return """Generated Password: {} """.format(self.password)
        else:
            return "No password is generated yet"


def main():

    cli = CLI()
    args = cli.parse_args()
    cache = Cache()
    generator = PasswordGenerator()

    if args.command in ('c', 'clear', 'wipe'):
        cache.emptyCache()
        print("Cache file is now empty")
        exit(0)

    if args.command in ('list', 'ls', 'l'):
        cachedPasswords = cache.getRecentPasswords(args.limit)
        if len(cachedPasswords):
            for record in cachedPasswords:
                print("Time: {}, Password: {}".format(record[0], record[1]))
        else:
            print("Cache file is empty")
        exit(0)

    if args.command in ('g', 'gen', 'generate'):
        password_complexity = Complexity.ALPHANUMERIC
        if args.alpha:
            password_complexity = Complexity.ALPHA
        if args.num:
            password_complexity = Complexity.NUMERIC
        if args.complex:
            password_complexity = Complexity.HARD
        generator = PasswordGenerator(password_complexity, args.length)

    generatedPassword = generator.generate()
    cache.storePassword(generatedPassword)
    print("Generated password: " + generatedPassword)
    exit(0)


if __name__ == "__main__":
    main()
