import json
from argparse import ArgumentParser
from fuzzyfinder import fuzzyfinder


class CommandParser(object):
    """ CommandParser will parse the tokens of the kubectl command tree """
    def __init__(self, api_json=None):
        self.api_schema = dict()
        with open(api_json) as fd:
            self.api_schema = json.load(fd)
        self.parser = ArgumentParser(prog='kubectl')
        self.walk(self.parser, self.api_schema)

    def walk(self, root_parser, command):
        """ Walks the API JSON schema """
        for cmd, details in command.items():
            subparser = root_parser.add_subparsers()
            if details.get('subcommands') and details['subcommands']:
                for subcmd, subdetails in details['subcommands'].items():
                    child_parser = subparser.add_parser(subcmd)
                    print("subcommand: %s" % subcmd)
                    self.walk(child_parser, subdetails)
            elif details.get('args') and details['args']:
                for arg in details.get('args'):
                    subparser.add_parser(arg)
            else:
                if details.get('options') and not details['options']:
                    for key, value in details.get('options').items():
                        root_parser.add_argument(key, help=value.get('help'))


if __name__ == '__main__':
    CommandParser('data/cli.json')
