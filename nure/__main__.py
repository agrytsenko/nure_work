import sys

from fetcher import download_page
from splitter import translate_page


def main(site_url):
    p = download_page(site_url)
    r = translate_page(p)
    print '\n\nResult saved to: ' + r + '\n\n'

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print '\n\tUsage: python nure <url>\n'
        sys.exit(0)
    main(args[0])
