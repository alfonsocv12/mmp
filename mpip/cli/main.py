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
    except NoSuchCommand as e:
        pass_to_lib()
    except Exception as e:
        print(str(e))

def pass_to_lib():
    '''
    Function dedicated to pass commands to the virtualenviroment
    '''
    lib_command: str = ' '.join(sys.argv[1:])
    os.system(f'pip_modules/bin/{lib_command}')
    return

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
    '''Install and handle your pip dependencies fast and easy

    usage:
        mpip [options] [--] [COMMAND] [ARGS...]
        mpip -h|--help

    Options:
        -v, --version            Shows mpip version

    Commands:
        install                  Install your libraries on pip_modules
        init                     Create requirements.txt to to add python libraries
    '''

    def __init__(self, options=None):
        '''
        Constructor function
        '''
        self.toplevel_options = options or {}

    def install(self, options=None):
        '''
        Install commands installs all your libraries on a pip_modules forder

        Usage: install [options] [COMMAND]
        '''
        if options.get('COMMAND', None):
            print(options)
            bcolors.printColor(
                'WARNING', 'We will build a package installer on the future'
            )
            return

        bcolors.printColor('OKGREEN', 'Start installing libraries')
        if not os.path.exists('pip_modules/'): self.__create_virtualenv()
        bcolors.printColor('OKCYAN', 'Start installing libraries')
        if not os.path.exists('requirements.txt'):
            bcolors.printColor('FAIL', 'missing requirements.txt')
            bcolors.printColor('UNDERLINE', 'YOU could run this command')
            bcolors.printColor('OKBLUE', '  $ mpip init')
        os.system("./pip_modules/bin/pip install -r requirements.txt")
        bcolors.printColor('OKGREEN', 'Finish installation')

    def init(self, options=None):
        '''
        Init the mpip environment

        For example:
            $ mpip init

        By default, creates the virtualenv in pip_modules dir on the proyect
        and a requirements.txt without any line on the requirements file

        usage: init
        '''
        bcolors.printColor('OKGREEN', 'Initializing mpip')
        if not os.path.exists("pip_modules/"):
            self.__create_virtualenv()
        if not os.path.exists('requirements.txt'):
            bcolors.printColor('OKCYAN', 'Creating requirements.txt')
            open("requirements.txt", "w").close()
        bcolors.printColor('OKGREEN', 'Finish init')

    def __create_virtualenv(self):
        '''
        Function dedicated to create a new virtual env with the name
        '''
        bcolors.printColor('OKCYAN', 'Creating virtualenv')
        os.system("virtualenv --python=python3 pip_modules")


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
