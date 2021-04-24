import os
import mpip

def get_version_info(scope):
    versioninfo = 'mpip version {}, build {}'.format(
        mpip.__version__, get_build_version()
    )

    if scope == 'mpip':
        return versioninfo
    # if scope == 'full':
    #     return (
    #         "{}\n"
    #         "docker-py version: {}\n"
    #         "{} version: {}\n"
    #         "OpenSSL version: {}"
    #     ).format(
    #         versioninfo,
    #         docker.version,
    #         platform.python_implementation(),
    #         platform.python_version(),
    #         ssl.OPENSSL_VERSION)

    raise ValueError("{} is not a valid version scope".format(scope))

def get_build_version():
    filename = os.path.join(os.path.dirname(mpip.__file__), 'GITSHA')
    if not os.path.exists(filename):
        return 'unknown'

    with open(filename) as fh:
        return fh.read().strip()
