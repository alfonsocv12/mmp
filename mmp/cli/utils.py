import os
import mmp

def get_version_info(scope):
    versioninfo = 'mmp version {}'.format(mmp.__version__)

    if scope == 'mmp':
        return versioninfo

    raise ValueError("{} is not a valid version scope".format(scope))
