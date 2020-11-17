import random
import enum

ALPHA = [chr(i) for i in range(97, 123)] + [chr(i).upper() for i in range(97, 123)]
NUMERIC = [str(i) for i in range(10)]
ALPHANUMERIC = ALPHA + NUMERIC
HARD = ["!", "@", "#", "$", "%", "^", "&", "*", "_", "-", ";", ",", "."] + ALPHANUMERIC


class Complexity(enum.Enum):
    ALPHA = 1
    NUMERIC = 2
    ALPHANUMERIC = 3
    HARD = 4

class Generator:
    def __init__(self, complexity=Complexity.ALPHANUMERIC, length=16):
        self.complexity = complexity
        self.length = length
        self.generated = None

    def generate(self):
        if repr(self.complexity) == repr(Complexity.ALPHA):
            self.generated = self.generate_alpha()

        if repr(self.complexity) == repr(Complexity.ALPHANUMERIC):
            self.generated = self._generateAlphaNumeric()

        if repr(self.complexity) == repr(Complexity.NUMERIC):
            self.generated = self.generate_num()

        if repr(self.complexity) == repr(Complexity.HARD):
            self.generated = self._generateHard()

        return self.generated

    def generate_alpha(self) -> str:
        password = ""
        for i in range(self.length):
            password += ALPHA[random.randint(0, len(ALPHA) - 1)]
        return password

    def generate_num(self):
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
        if self.generated:
            return """Generated Password: {} """.format(self.generated)
        else:
            return "No password is generated yet"
