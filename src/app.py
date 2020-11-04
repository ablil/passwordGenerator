###########################################################
# Script Name	: passwordGenerator.py
# Description	: random custom password generator
# Arguments	: passwordGenerator.py --recent 4 --alpha --numeric --alphanumric --hard --length 5 --delete-cache
# Date		: 2020-03-18
# Author	: ablil
# Email		: ablil@protonmail.com
###########################################################

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


class Parser:
    def __init__(self):
        self.passwordLength = 15
        self.passwordComplexity = None
        self.emptyCache = False
        self.recentCache = 0

    def parse(self):
        parser = self._createParser()
        args = parser.parse_args()

        if args.alpha:
            self.passwordComplexity = Complexity.ALPHA
        if args.alphanumeric:
            self.passwordComplexity = Complexity.ALPHANUMERIC
        if args.numeric:
            self.passwordComplexity = Complexity.NUMERIC
        if args.hard:
            self.passwordComplexity = Complexity.HARD

        if args.recent:
            self.recentCache = args.recent[0]

        if args.empty_cache:
            self.emptyCache = True

        if args.length:
            self.passwordLength = args.length[0]

        # options from both groups are not allowed
        if self.passwordComplexity and (self.emptyCache or self.recentCache):
            parser.print_help()
            exit(1)

    def _createParser(self) -> argparse:
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-l",
            "--length",
            nargs=1,
            type=int,
            help="Password length (default: {})".format(self.passwordLength),
        )

        # group 1
        complexityParser = parser.add_mutually_exclusive_group()
        complexityParser.add_argument(
            "--alpha",
            action="store_true",
            help="use alphanumeric characters only (uppercase / lowercase",
        )
        complexityParser.add_argument(
            "--numeric", action="store_true", help="use numeric values only"
        )
        complexityParser.add_argument(
            "--alphanumeric",
            action="store_true",
            help="user characters and numebrs. (This is the default option)",
        )
        complexityParser.add_argument(
            "--hard",
            action="store_true",
            help="use characters, numbers and symbols (Recommanded)",
        )

        # group 2
        cacheParser = parser.add_mutually_exclusive_group()
        cacheParser.add_argument(
            "--recent", nargs=1, type=int, help="Get recent generated passwords"
        )
        cacheParser.add_argument(
            "--empty-cache", action="store_true", help="Empty Cache"
        )

        return parser

    def usage(self):
        self._createParser().print_help

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

    parser = Parser()
    parser.parse()
    cache = Cache()
    generator = PasswordGenerator()

    if parser.emptyCache:
        cache.emptyCache()
        print("Cache file is now empty")
        exit(0)

    if parser.recentCache != 0:
        cachedPasswords = cache.getRecentPasswords(parser.recentCache)
        if len(cachedPasswords):
            for record in cachedPasswords:
                print("Time: {}, Password: {}".format(record[0], record[1]))
        else:
            print("Cache file is empty")
        exit(0)

    if parser.passwordComplexity:
        generator = PasswordGenerator(parser.passwordComplexity, parser.passwordLength)

    generatedPassword = generator.generate()
    cache.storePassword(generatedPassword)
    print("Generated password: " + generatedPassword)
    exit(0)


if __name__ == "__main__":
    main()
