

WORKING_DIR = '/tmp'

# on different OS `wget` might be installer either
# /us/bin/wget of /us/local/bin/wget etc..
try:
    import subprocess

    WGET_BIN = subprocess.check_output([
        "/bin/sh", "-c",
        "which wget ; exit 0"
    ], stderr=subprocess.STDOUT).strip()
except:
    WGET_BIN = '/usr/bin/wget'
finally:
    del subprocess

import subprocess
import sys

WGET_BIN = subprocess.check_output(
    ["/bin/sh", "-c", "which wget"],
    stderr=sys.stdout
).strip()

print type(WGET_BIN)
print repr(WGET_BIN)

WGET_PARAMS = (
    '--adjust-extension',
    '--span-hosts',
    '--convert-links',
    '--backup-converted',
    '--page-requisites',
    '--no-directories',
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


