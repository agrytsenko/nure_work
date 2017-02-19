from __future__ import unicode_literals

import os
import re
import logging
from functools import wraps

import bs4
from translate import translate, json_translate


log = logging.getLogger()
sep = '-' * 40

TRANSLATABLE = 'p', 'i', 'b', 'h1', 'h2', 'h3', 'dd', 'dl', 'dt', 'li'  # 'a', 'span
RE_CHAR = re.compile(r'.*\w+.*', re.UNICODE)


visited = lambda e: setattr(e, '__visited', True) or e

is_visited = lambda e: getattr(e, '__visited', None) is True


def debug_trs(f):
    @wraps(f)
    def inner(text, *args):
        res = f(text, *args)
        res is not None and log.debug('%s\n%s\n', sep, text)
        return res
    return inner


@debug_trs
def do_trs(text, lang='ru'):
    try:
        return json_translate(text, lang)
    except (IOError, KeyError):
        pass
    try:
        return translate(text, lang)
    except (IOError, KeyError) as e:
        pass
    return e


def translate_tag(tag):

    for i, el in enumerate(tag.contents):
        if isinstance(el, bs4.Tag):
            tag.contents[i] = translate_tag(el)
            continue

        if tag.name not in TRANSLATABLE:
            continue

        if isinstance(el, bs4.NavigableString):
            if is_visited(el):
                continue
            s = unicode(el)
            if not re.match(RE_CHAR, s):
                continue
            tr = do_trs(s)
            if tr is None:
                continue
            tag.contents[i] = visited(bs4.NavigableString(tr))

    return tag


def translate_html(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    top_level_tags = soup.find_all(TRANSLATABLE)
    for tag in top_level_tags:
        translate_tag(tag)
    return soup.prettify("utf-8")


def get_html(file_path):
    with open(file_path) as f:
        return f.read()


def store_html(html, file_path, res_file='result.html'):
    res_file = os.path.join(os.path.dirname(file_path), res_file)
    with open(res_file, 'w') as f:
        f.write(html)
    return res_file


def translate_page(file_path):
    html_content = get_html(file_path)
    translated = translate_html(html_content)
    return store_html(translated, file_path)


if __name__ == '__main__':
    p = '/Users/alexander/Desktop/docs.python.org/re.html'
    t = get_html(p)
    r = translate_html(t)
    out_file = store_html(r, p)



