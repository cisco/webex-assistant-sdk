import argparse
import getpass
import os
import pprint
import shutil


class PasswordPromptAction(argparse.Action):
    def __init__(  # pylint: disable=redefined-builtin,too-many-arguments
        self,
        option_strings,
        dest=None,
        nargs=0,
        const=None,
        default=None,
        type=None,
        choices=None,
        required=False,
        help=None,
        metavar=None,
        prompt=None,
    ):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            const=const,
            default=default,
            type=type,
            choices=choices,
            required=required,
            metavar=metavar,
            help=help,
        )
        self.prompt = prompt or f'{self.dest.capitalize()}: '

    def __call__(self, parser, args, values, option_string=None):
        password = getpass.getpass(self.prompt)
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
        help='a password to encrypt the private key',
    )

    invoke_parser = subparsers.add_parser(
        'invoke', help='invoke a skill simulating a request from Webex Assistant'
    )
    invoke_parser.add_argument('text', help='the message for the skill')
    invoke_parser.add_argument(
        '-s',
        '--secret',
        type=str,
        action=PasswordPromptAction,
        help="the skill's secret",
        required=True,
        prompt='Skill Secret: ',
    )
    invoke_parser.add_argument(
        '-k', '--key-file', help="the path to the skill's public key file on disk", required=True
    )
    invoke_parser.add_argument(
        '-U',
        '--url',
        default='http://localhost:7150/parse',
        help='the URL where the skill is served',
    )

    return parser


def generate_keys(filename, key_type, password=None):
    from . import crypto  # pylint: disable=import-outside-toplevel

    filename = os.path.abspath(filename)
    print(f'Generating {key_type} keys at {filename!r}')

    crypto.generate_keys(filename, key_type, password)
    print('done')


def invoke_agent(secret, key_file, text, url):
    from . import crypto, helpers  # pylint: disable=import-outside-toplevel

    public_key = crypto.load_public_key_from_file(key_file)

    try:
        res = helpers.make_request(secret, public_key, text, url=url)
        directives = res.get('directives')
    except Exception:  # pylint: disable=broad-except
        print(f'Failed to invoke skill at {url}')
        return

    print(f'Successfully invoked skill at {url}')

    width = shutil.get_terminal_size((80, 20))[0]
    print('Response: ')
    pprint.pprint(directives, indent=2, width=width)


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.command == 'new':
        print("\n\nNot yet implemented")
        return

    if args.command == 'generate-keys':
        generate_keys(args.filename, args.key_type, args.password)
        return

    if args.command == 'invoke':
        invoke_agent(args.secret, args.key_file, args.text, url=args.url)
        return

    parser.print_help()


if __name__ == '__main__':
    main()
