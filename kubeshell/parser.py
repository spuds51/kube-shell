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

    def walk(self, root_parser, command, indent=0):
        """ Walks the API JSON schema """
        subparser = root_parser.add_subparsers()
        cmd, details = command.items().pop()
        if details.get('subcommands') and details['subcommands']:
            for subcmd, subdetails in details['subcommands'].items():
                child_parser = subparser.add_parser(subcmd, help=subdetails['help'])
                if len(subdetails) == 1:
                    self.walk(child_parser, subdetails, indent+1)
                if subdetails.get('args') and subdetails['args']:
                    for arg in subdetails['args']:
                        subparser.add_parser(arg)
                if subdetails.get('options') and subdetails['options']:
                    for key, value in subdetails['options'].items():
                        child_parser.add_argument(key, help=value.get('help'))


if __name__ == '__main__':
    CommandParser('data/cli.json')
