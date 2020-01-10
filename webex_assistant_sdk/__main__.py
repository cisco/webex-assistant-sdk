import argparse
import getpass
import os


class PasswordPromptAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        password = getpass.getpass()
        setattr(args, self.dest, password)


def get_parser():
    parser = argparse.ArgumentParser('wxa_sdk')

    subparsers = parser.add_subparsers(dest='command')

    new_parser = subparsers.add_parser('new', help='create a new skill project')
    new_parser.add_argument('name', help='the name of the skill', metavar='skill-name')
    keys_parser = subparsers.add_parser(
        'generate-keys', help='generate keys for use with a Webex Assistant Skill'
    )
    keys_parser.add_argument('filename', help='the name of the private key')
    keys_parser.add_argument(
        '-t',
        '--type',
        default='rsa',
        dest='key_type',
        choices=['rsa', 'ed25519'],
        help='the type of SSH key',
    )
    keys_parser.add_argument(
        '-p',
        '--password',
        default=None,
        type=str,
        action=PasswordPromptAction,
        help='an password to encrypt the private key',
    )

    return parser


def generate_keys(filename, key_type, password=None):
    from . import crypto  # pylint: disable=import-outside-toplevel

    filename = os.path.abspath(filename)
    print(f'Generating {key_type} keys at {filename!r}')

    crypto.generate_keys(filename, key_type, password)
    print('done')


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.command == 'new':
        print("\n\nNot yet implemented")
        return

    if args.command == 'generate-keys':
        generate_keys(args.filename, args.key_type, args.password)
        return

    parser.print_help()


if __name__ == '__main__':
    main()
