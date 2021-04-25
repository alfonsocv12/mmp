class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93mWARNING: '
    FAIL = '\033[91mFAIL: '
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def printColor(cls, type, message):
        print(f'{getattr(cls, type)}{message}{bcolors.ENDC}')
