import functools
import json
import os
import logging
import sys
from inspect import getdoc

from . import signals
from .colors import bcolors
from .docopt_command import DocoptDispatcher
from .docopt_command import get_handler
from .docopt_command import NoSuchCommand
from .formatter import ConsoleWarningFormatter
from .utils import get_version_info


log = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stderr)


def main():
    try:
        command = dispatch()
        command()
    except (KeyboardInterrupt, signals.ShutdownException):
        print("Aborting.")
        sys.exit(1)
    except Exception as e:
        print(str(e))


def dispatch():
    dispatcher = DocoptDispatcher(
        TopLevelCommand, {
            'options_first': True,
            'version': get_version_info('mpip')
        }
    )
    options, handler, command_options = dispatcher.parse(sys.argv[1:])
    return functools.partial(perform_command, options, handler, command_options)


def perform_command(options, handler, command_options):
    if options['COMMAND'] in ('help', 'version'):
        handler(command_options)
        return

    command = TopLevelCommand(options=options)
    # with errors.handle_connection_errors(project.client):
    handler(command, command_options)


class TopLevelCommand:
    '''Mpip pluging for pip for better handling your libraries

    usage:
        mpip [options] [--] [COMMAND] [ARGS...]
        mpip -h|--help

    Options:
        -v, --version           Print version and exit

    Commands:
        run                      Lets you run a specific query
        load-query               Load querys to db
        query                    List all queerys loaded
    '''

    def __init__(self, options=None):
        '''
        Constructor function
        '''
        self.toplevel_options = options or {}


    @classmethod
    def help(cls, options):
        """
        Get help on a command.

        Usage: help [COMMAND]
        """
        if options['COMMAND']:
            subject = get_handler(cls, options['COMMAND'])
        else:
            subject = cls

        print(getdoc(subject))


def set_no_color_if_clicolor(no_color_flag):
    return no_color_flag or os.environ.get('CLICOLOR') == "0"
