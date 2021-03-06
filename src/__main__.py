from .loader import Loader
from .cli import CLI
from .cache import Cache
from .generator import Generator
from .generator import Complexity


def main():

    cli = CLI()
    args = cli.parse_args()
    cache = Cache()
    generator = Generator()

    if args.command in ("c", "clear", "wipe"):
        cache.clear()
        print("All saved passwords are cleared")
        exit(0)

    if args.command in ("list", "ls", "l"):
        passwords = cache.list(args.limit)
        if len(passwords):
            for record in passwords:
                print(
                    f"Generated: {record['generated']}, password: {record['password']}"
                )
        else:
            print("No password is saved")
        exit(0)

    if args.command in ("export"):
        exporter = Loader(args.filename)
        passwords = cache.list()
        exporter.json_export(passwords)
        print(f"Exported all password to {args.filename}")

    if args.command in ("import"):
        importer = Loader(args.filename)
        imported_passwords = importer.json_import()
        for record in imported_passwords:
            cache.save(record["password"], record["generated"])

    if args.command in ("g", "gen", "generate"):
        password_complexity = Complexity.ALPHANUMERIC
        if args.alpha:
            password_complexity = Complexity.ALPHA
        if args.num:
            password_complexity = Complexity.NUMERIC
        if args.complex:
            password_complexity = Complexity.HARD
        generator = Generator(password_complexity, args.length)

        generatedPassword = generator.generate()
        cache.save(generatedPassword)
        print("Generated password: " + generatedPassword)


if __name__ == "__main__":
    main()