import enum
import argparse


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


if __name__ == "__main__":
    print("This is just an argument parser!!!")
