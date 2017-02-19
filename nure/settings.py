import subprocess
import logging
from logging.config import dictConfig


# WORKING_DIR = '/tmp'
WORKING_DIR = '/Users/alexander/Desktop/'

try:
    # on different OS `wget` might be installer either
    # /us/bin/wget of /us/local/bin/wget etc..
    WGET_BIN = subprocess.check_output([
        "/bin/sh", "-c",
        "which wget ; exit 0"
    ], stderr=subprocess.STDOUT).strip()
except:
    WGET_BIN = '/usr/bin/wget'


WGET_PARAMS = (
    '--adjust-extension',
    '--span-hosts',
    '--convert-links',
    '--backup-converted',
    '--page-requisites',
    '--no-directories',
    '--quiet',
)

WGET_CMD = (WGET_BIN, ) + WGET_PARAMS

USER_AGENT = (
    "Mozilla/4.0 ("
    "compatible;"
    "MSIE 6.0;"
    "Windows NT 5.1;"
    "SV1;"
    ".NET CLR 1.1.4322;"
    ".NET CLR 2.0.50727;"
    ".NET CLR 3.0.04506.30"
    ")"
)


LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
            # 'stream': 'ext: // sys.stdout',
        }
    },
    'formatters': {
        'simple': {
            'format': '%(message)s',
        },
        'default': {
            'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

dictConfig(LOGGING)
logging.getLogger("requests").setLevel(logging.WARNING)



