from .cli import CLI
import sys
import random
import enum
from .cache import Cache

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
        cache.clear()
        print("All saved passwords are cleared")
        exit(0)

    if args.command in ('list', 'ls', 'l'):
        passwords = cache.list(args.limit)
        if len(passwords):
            for record in passwords:
                print("Time: {}, Password: {}".format(record[0], record[1]))
        else:
            print("No password is saved")
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
    cache.save(generatedPassword)
    print("Generated password: " + generatedPassword)
    exit(0)


if __name__ == "__main__":
    main()
