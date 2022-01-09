import os
from .errors import (
    MissingFiles, MissingValue, NotSuchScript
)


class RunScripts:

    @staticmethod
    def get_run_script_value(command):
        '''
        Function dedicated to find the scripts on values

        param: command list
        '''
        try:
            import run as run_file
        except ImportError as e:
            raise Exception(f'Error on run.py: {str(e)}')
        except:
            raise MissingFiles('run.py')

        if not hasattr(run_file, 'SCRIPTS'):
            raise MissingValue('run.py', 'SCRIPTS')

        script_target: str = command[0]
        user_script: str = run_file.SCRIPTS.get(script_target, False)
        if not user_script:
            raise NotSuchScript(script_target)
        extra_args = ' '.join(command[1:])
        if extra_args:
            user_script = f'{user_script} {extra_args}'
        os.system(f'pip_modules/bin/{user_script}')
        return
