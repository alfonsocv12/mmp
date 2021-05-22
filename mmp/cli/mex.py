import functools
import json
import re
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
    except NoSuchCommand as e:
        TopLevelCommand.pass_to_lib()
    except Exception as e:
        print(str(e))

def dispatch():
    dispatcher = DocoptDispatcher(
        TopLevelCommand, {
            'options_first': True,
            'version': get_version_info('mmp')
        }
    )
    options, handler, command_options = dispatcher.parse(sys.argv[1:])
    return functools.partial(perform_command, options, handler, command_options)


def perform_command(options, handler, command_options):
    if options['COMMAND'] in ('help', 'version'):
        handler(command_options)
        return

    command = TopLevelCommand(options=options)
    handler(command, command_options)


class TopLevelCommand:
    '''Module Environment Executor

    This is the short for mmp exec, running a command from local modules

    usage:
        mex [options] [--] [COMMAND] [ARGS...]
        mex -h|--help

    Options:
        -v, --version            Shows mmp version
    '''

    def __init__(self, options=None):
        '''
        Constructor function
        '''
        self.toplevel_options = options or {}

    @staticmethod
    def pass_to_lib():
        '''
        Function dedicated to pass commands to the virtualenviroment
        '''
        command_to_find: str = sys.argv[1]
        full_command: str = ' '.join(sys.argv[1:])
        try:
            if not os.path.isfile(f'pip_modules/bin/{command_to_find}'):
                raise NoSuchCommand(command_to_find, 'aol')

            os.system(f'pip_modules/bin/{full_command}')
        except Exception as e:
            print(str(e))
        return

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
