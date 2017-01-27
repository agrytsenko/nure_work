# -*- coding: utf-8 -*-
import re

import urllib2
import urllib
from HTMLParser import HTMLParser


# from bs4 import BeautifulSoup
#
# http://py-translate.readthedocs.io/en/latest/devs/api.html
# https://github.com/jjangsangy/py-translate/blob/master/translate/translator.py
#
# http://stackoverflow.com/a/14694669
#
# http://stackoverflow.com/questions/14369447/how-to-save-back-changes-made-to-a-html-file-using-beautifulsoup-in-python
#


agent_header = (
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


def translate(text, to_lang='auto', from_lang='auto'):
    """Returns the translation using google translate
    you must shortcut the language you define
    (French = fr, English = en, Spanish = es, etc...)
    if not defined it will detect it or use english by default

    Example:
        >>> translate('hello there!', 'ru')
        Привет!
    """
    base_link = 'http://translate.google.com/m?hl=%s&sl=%s&q=%s'
    to_translate = urllib.quote_plus(text)
    link = base_link % (to_lang, from_lang, to_translate)
    request = urllib2.Request(link, headers=agent)
    raw_data = urllib2.urlopen(request).read()

    data = raw_data.decode("utf-8")
    expr = r'class="t0">(.*?)<'
    re_result = re.findall(expr, data)
    if len(re_result) == 0:
        result = ''
    else:
        result = HTMLParser().unescape(re_result[0])
    return result


if __name__ == '__main__':
    print translate('hello there!', 'zh_cn')
    print translate('hello there!', 'ja')
    print translate('hello there!', 'ru')
