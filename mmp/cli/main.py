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
    # with errors.handle_connection_errors(project.client):
    handler(command, command_options)


class TopLevelCommand:
    '''Install and handle your pip dependencies fast and easy

    usage:
        mmp [options] [--] [COMMAND] [ARGS...]
        mmp -h|--help

    Options:
        -v, --version            Shows mmp version

    Commands:
        run                      Run python files with the environment modules
        install                  Install your libraries on pip_modules
        init                     Create requirements.txt to to add python libraries
        upgrade                  Upgrade module on the pip_modules
        uninstall                remove libraries from pip_modules
        clean                    Clean all the libraries and reinstall requirements
    '''

    def __init__(self, options=None):
        '''
        Constructor function
        '''
        self.toplevel_options = options or {}

    def run(self, options=None):
        '''
        Run python files with the enviroment modules

        usage: run [<file>]
        '''
        file = options.get('<file>', None)
        if file:
            os.system(f'pip_modules/bin/python {file}')
            return
        if not os.path.exists('run.py'):
            bcolors.printColor('FAIL', 'Missing run.py or file parameter')
            return
        os.system('pip_modules/bin/python run.py')

    def install(self, options=None):
        '''
        Install commands installs all your libraries on a pip_modules forder

        Usage: install [options] [COMMAND]
        '''
        if options.get('COMMAND', None):
            self.__install_specifict_lib(options.get('COMMAND'))
            return

        bcolors.printColor('HEADER', 'Start install')
        self.__check_virtual_env()
        print('Running pip install')
        if not os.path.exists('requirements.txt'):
            bcolors.printColor('FAIL', 'missing requirements.txt')
            print('\nSUGGESTION: This command could help')
            print('  $ mmp init')
            return
        os.system("./pip_modules/bin/pip install -r requirements.txt")
        bcolors.printColor('OKGREEN', 'Finish installation')

    def init(self, options=None):
        '''
        Init the mmp environment

        For example:
            $ mmp init

        By default, creates the virtualenv in pip_modules dir on the proyect
        and a requirements.txt without any line on the requirements file

        usage: init
        '''
        bcolors.printColor('HEADER', 'Initializing mmp')
        self.__check_virtual_env()
        self.__check_requirements()
        bcolors.printColor('OKGREEN', 'Finish init')

    def uninstall(self, options=None):
        '''
        Uninstall a lib from the pip_modules

        For example:
            $ mmp uninstall mmp

        usage: uninstall [COMMAND]
        '''
        if not options.get('COMMAND', None):
            bcolors.printColor('FAIL', 'You need to send the module name')
            return
        self.__uninstall_pip_module(options.get('COMMAND'))

    def clean(self, options=None):
        '''
        Clean all the libraries and reinstall the requirements.txt

        usage: clean
        '''
        if not os.path.exists('pip_modules'):
            bcolors.printColor('FAIL', 'No pip_modules')
            return
        if not os.path.exists('requirements.txt'):
            bcolors.printColor('FAIL', 'No requirements.txt')
            return
        os.system('rm -rf pip_modules')
        self.__check_virtual_env()
        os.system('pip_modules/bin/pip install -r requirements.txt')

    def upgrade(self, options=None):
        '''
        Upgrade specific module on the pip_modules

        usage: upgrade [COMMAND]
        '''
        if not options.get('COMMAND', None):
            bcolors.printColor('FAIL', 'Missing module to upgrade')
            return
        module_name = options.get('COMMAND')
        os.system(f'pip_modules/bin/pip install --upgrade {module_name}')

    def __uninstall_pip_module(self, module_name: str):
        '''
        This function deletes the module from pip_modules and remove it from
        requirements
        '''
        if not os.path.exists("pip_modules/"):
            bcolors.printColor('FAIL', 'Can\'t remove module')
            return
        os.system(f'pip_modules/bin/pip uninstall {module_name}')
        self.__update_requirements(module_name, remove=True)

    def __check_virtual_env(self):
        '''
        Function dedicated to create a new virtual env with the name
        '''
        if not os.path.exists("pip_modules/"):
            print('Creating virtualenv')
            os.system('virtualenv --python=python3 pip_modules')

    def __check_requirements(self):
        '''
        Check requirements file if not create
        '''
        if not os.path.exists('requirements.txt'):
            print('Creating requirements.txt')
            open('requirements.txt', 'w').close()

    def __install_specifict_lib(self, command: str):
        '''
        Here we pass a install command to pip to install a librari into our
        pip_modules and adding it into our requirements.txt

        param: options (dict)
        '''
        self.__check_virtual_env()
        self.__check_requirements()
        lib: dict = {
            'name': command.rstrip('\x00').split('=')[0],
        }
        v_installed = self.__check_lib_installed(lib['name'])
        if v_installed:
            bcolors.printColor('WARNING', f'{v_installed} allready satisfied')
            return
        os.system(f'pip_modules/bin/pip install {command}')
        show_result = os.popen(f'pip_modules/bin/pip show {lib["name"]}').read()
        lib['version'] = show_result.splitlines()[1].split(':')[1].strip(' ')
        self.__update_requirements(lib['name'], lib['version'])

    def __update_requirements(self, name: str, version=None, remove=False):
        '''
        Function dedicated to update requirements.txt with the new lib
        '''
        requirements = open('requirements.txt', 'r+')
        requirements_read: list = requirements.readlines()
        if remove:
            for i, s in enumerate(requirements_read):
                if name in s:
                    del requirements_read[i]
        else:
            if not name in requirements_read:
                requirements_read.append(
                    f'{name}=={version}\n'
                )
        requirements_write = ''.join(sorted(requirements_read))
        requirements.truncate(0)
        requirements.write(requirements_write)
        requirements.close()

    def __check_lib_installed(self, lib_name: str):
        '''
        Function dedicated to check if lib allready in pip_modules
        '''
        response = os.popen(
            'pip_modules/bin/python -c "from pip._internal.commands.show import search_packages_info\n'
            'exist = False\n'
            f'for i, dist in enumerate(search_packages_info([\'{lib_name}\'])):\n'
            ' exist = True\n'
            ' name = dist.get(\'name\', False)\n'
            ' version = dist.get(\'version\', False)\n\n'
            'if exist:\n'
            ' print(f\'{name}, {version}\')\n\n'
            'else:'
            ' print(\'False\')"'
        )
        response_str: str = response.read().strip('')
        if 'False' in response_str:
            return
        return response_str.rstrip('\n')

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
