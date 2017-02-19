import os
import sys
import shutil
import logging
import subprocess
from urlparse import urlparse

from settings import WORKING_DIR, WGET_CMD


log = logging.getLogger(__name__)


def mkdir(path):
    """Crete directory on file system. Overrides existing one """
    if not path.startswith(WORKING_DIR):
        path = os.path.join(WORKING_DIR, path)
    if os.path.isdir(path):
        shutil.rmtree(path)
    log.debug('Creating a directory: %s', path)
    os.makedirs(path)
    return path


def check_url(url):
    """URL should always start with `http` prefix. Add prefix if not specified """
    if not url.startswith('http'):
        log.warn('Incorrect URL syntax. URL should start with http/https')
        url = 'http://' + url
        log.warn('Using URL=%s' % url)
    return url


def parse_url(url):
    try:
        return urlparse(url)
    except Exception as e:
        log.error(e.message)
        sys.exit(1)


def get_index_page(work_dir, url, default='index.html'):
    """Returns absolute path to an index page of downloaded resource """
    uu = parse_url(url)
    if not uu.path:
        index = default
    elif '/' not in uu.path:
        index = default
    else:
        index = uu.path.split('/')[-1]
    return os.path.join(work_dir, index)


def fetch_url(url, to_dir):
    cmd = WGET_CMD + (url, )
    ret_code = subprocess.call(
        cmd,
        cwd=to_dir,
        stdout=sys.stdout,
        stderr=sys.stdout)
    return ret_code


def download_page(url):
    url = check_url(url)
    uu = parse_url(url)
    site_dir = mkdir(uu.netloc)
    fetch_url(url, site_dir)
    return get_index_page(site_dir, url)


if __name__ == '__main__':
    u = 'docs.python.org/2/library/urlparse.html'
    buggy = 'https://docs.python.org/3/distributing/index.html'
    print download_page(u)

