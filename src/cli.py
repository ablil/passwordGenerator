import argparse

USAGE = """
USAGE:
core commands:
    generate:   generate passwords
    list:       list recent generated password
    clear:      clear store passwords
    import:     import passwords from json file
    export:     export password to json file

command aliases:
    generate:   g, gen, generate
    list:       l, ls, list
    clear:      c, clear, wipe
"""

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="qpg",
            epilog=f"For more info: https://github.com/ablil/quick-password-generator",
        )

        self.subparsers = self.parser.add_subparsers(
            help="core commands help", dest="command"
        )

        self.generate()
        self.list()
        self.clear()
        self.import_json()
        self.export_json()

    def generate(self):
        """Full CLI command to generate password"""
        parser_generate = self.subparsers.add_parser(
            "generate", aliases=["g", "gen"], description="Generate passwords"
        )
        general_group = parser_generate.add_argument_group("General")
        general_group.add_argument(
            "-l", "--length", default=16, type=int, help="password length (Default: 16)"
        )
        complexity_group = parser_generate.add_argument_group(
            "complexity", "Password generation strategy (Optional)"
        )
        password_complexity = complexity_group.add_mutually_exclusive_group()
        password_complexity.add_argument(
            "--alpha", action="store_true", help="alphabets only"
        )
        password_complexity.add_argument(
            "--num", action="store_true", help="numbers only"
        )
        password_complexity.add_argument(
            "--alphanum",
            action="store_true",
            help="alphabets and numbers (Default)",
        )
        password_complexity.add_argument(
            "--complex", action="store_true", help="arlphabets, number and symbols"
        )

    def list(self):
        """Full CLI command to list previous generated passwords"""
        parser_list = self.subparsers.add_parser(
            "list", aliases=["l", "ls"], description="List generated passwords"
        )
        parser_list.add_argument(
            "-l",
            "--limit",
            default=-1,
            type=int,
            help="number of passwords to show(Default: all)",
        )

    def clear(self):
        """Full CLI command to clear store passwords"""
        parser_clear = self.subparsers.add_parser(
            "clear", aliases=["c", "wipe"], description="Clear stored passwords"
        )

    def import_json(self):
        """FUll CLI command to import passwords from json file"""
        import_parser = self.subparsers.add_parser('import', description='Import passwords from json file')
        import_parser.add_argument('filename', type=str, help="json filename")

    def export_json(self):
        """Full cli command to export saved passwords"""
        export_parser = self.subparsers.add_parser('export', description='Export password from json file')
        export_parser.add_argument('filename', type=str, help='Json filename')

    def parse_args(self):
        args = self.parser.parse_args()
        if not args.command:
            print(USAGE)
            exit(0)
        return args