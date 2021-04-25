import os
import mpip

def get_version_info(scope):
    versioninfo = 'mpip version {}'.format(mpip.__version__)

    if scope == 'mpip':
        return versioninfo

    raise ValueError("{} is not a valid version scope".format(scope))
