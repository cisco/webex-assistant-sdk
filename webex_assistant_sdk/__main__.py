import argparse
import getpass
import json
from pathlib import Path
import pprint
import shutil
import sys
import textwrap

from . import crypto, helpers


class PasswordPromptAction(argparse.Action):
    def __init__(  # pylint: disable=redefined-builtin,too-many-arguments
        self,
        option_strings,
        dest=None,
        nargs='?',
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
        if values:
            password = values
        else:
            password = getpass.getpass(self.prompt)

        setattr(args, self.dest, password)


def get_parser():
    parser = argparse.ArgumentParser('wxa_sdk')

    subparsers = parser.add_subparsers(dest='command')

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

    new_parser = subparsers.add_parser(
        'new',
        help='create a new skill project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            '''\
            This command creates a simple skill project based on a scaffold template.
            The skill_name should follow snakecase format because it is used for the
            package filename as well.
            '''
        ),
    )
    new_parser.add_argument('skill_name', help='the name of the skill.', metavar='skill-name')
    new_parser.add_argument(
        'secret',
        type=str,
        help='a secret string used for your skill application',
        action=PasswordPromptAction,
    )
    new_parser.add_argument(
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
    invoke_parser.add_argument(
        '-s',
        '--secret',
        type=str,
        action=PasswordPromptAction,
        help="the skill's secret",
        prompt='Enter skill secret: ',
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
    invoke_parser.add_argument(
        '-c', '--context', default=None, help='the JSON context to use in the invocation'
    )
    invoke_parser.add_argument(
        '-f', '--frame', default=None, help='the JSON frame to use in the invocation'
    )

    check_parser = subparsers.add_parser(
        'check', help='check the health and configuration of a Webex Assistant Skill'
    )
    check_parser.add_argument(
        '-s',
        '--secret',
        type=str,
        action=PasswordPromptAction,
        help="the skill's secret",
        prompt='Enter skill secret: ',
    )
    check_parser.add_argument(
        '-k', '--key-file', help="the path to the skill's public key file on disk", required=True
    )
    check_parser.add_argument(
        '-U',
        '--url',
        default='http://localhost:7150/parse',
        help='the URL where the skill is served',
    )
    return parser


def new_skill(skill_name: str, secret: str, password=None):
    from cookiecutter.main import cookiecutter  # pylint: disable=import-outside-toplevel
    import re  # pylint: disable=import-outside-toplevel

    def _validate_skill_name(name: str) -> bool:
        package_pattern = re.compile(r'[a-z][a-z0-9_]*')
        return bool(package_pattern.fullmatch(name))

    invoke_location = Path().resolve()
    package_location = Path(__file__).resolve()

    # Format the skill_name; Do not allow spaces
    if not _validate_skill_name(skill_name):
        print('Please use snakecase to name your skill')

    # TODO: Add logic to use MM-less template when available
    template_path = package_location.parent / 'templates/mindmeld_template'

    rsa_filename: str = f'{skill_name}.id_rsa'
    cookiecutter(
        str(template_path),
        output_dir=str(invoke_location),
        no_input=True,
        extra_context={
            'skill_name': skill_name,
            'rsa_file_name': rsa_filename,  # Path to the RSA key
            'rsa_password': password,
            'app_secret': secret,
        },
    )


def invoke_skill(secret, key_file, url, context=None, frame=None):
    public_key = crypto.load_public_key_from_file(key_file)

    history = []
    first = True
    while True:
        try:
            prompt = 'Enter command for skill\n' if first else ''
            first = False
            text = input(f'{prompt}>>> ')
            res = helpers.make_request(
                secret, public_key, text, context=context, frame=frame, history=history, url=url
            )
            directives = res.get('directives')
            context = res.get('context')
            frame = res.get('frame')
            history = res.get('history', [])
        except Exception as exc:  # pylint: disable=broad-except
            print(exc)
            print(f'Failed to invoke skill at {url}')
            return
        except KeyboardInterrupt:
            return

        width = shutil.get_terminal_size((80, 20))[0]
        print('Response: ')
        pprint.pprint(directives, indent=2, width=width)


def check_skill(secret, key_file, url):
    public_key = crypto.load_public_key_from_file(key_file)

    res = helpers.make_health_check(secret, public_key, url)
    print(res)


def parse_json_argument(name, arg):
    try:
        return json.loads(arg)
    except json.JSONDecodeError:
        print(f'Unable to decode {name!r} argument JSON')
        sys.exit(1)


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.command == 'new':
        new_skill(args.skill_name, args.secret, args.password)
        return

    if args.command == 'invoke':
        if not args.secret:
            # reparse with added '-s'
            # Note: for some reason we have to pop off the first arg when reparsing
            args = parser.parse_args(args=sys.argv[1:] + ['-s'])

        context = parse_json_argument('context', args.context) if args.context else None
        frame = parse_json_argument('frame', args.frame) if args.frame else None
        invoke_skill(args.secret, args.key_file, url=args.url, context=context, frame=frame)
        return

    if args.command == 'check':
        if not args.secret:
            # reparse with added '-s'
            # Note: for some reason we have to pop off the first arg when reparsing
            args = parser.parse_args(args=sys.argv[1:] + ['-s'])
        check_skill(args.secret, args.key_file, url=args.url)
        return

    parser.print_help()


if __name__ == '__main__':
    main()
