# -*- coding: utf-8 -*-
import re

import json
import requests
import urllib2
import urllib
from HTMLParser import HTMLParser
from requests.adapters import HTTPAdapter


# from bs4 import BeautifulSoup
#
# http://py-translate.readthedocs.io/en/latest/devs/api.html
# https://github.com/jjangsangy/py-translate/blob/master/translate/translator.py
#
# http://stackoverflow.com/a/14694669
#
# http://stackoverflow.com/questions/14369447/how-to-save-back-changes-made-to-a-html-file-using-beautifulsoup-in-python
#

URL = 'http://translate.google.com/m?hl=%s&sl=%s&q=%s'
URL_JSON = 'https://translate.google.com/translate_a/single'

user_agent = (
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

content_type = 'application/json; charset=utf-8'


def translate(text, to_lang='auto', from_lang='auto'):
    """Returns the translation using google translate
    you must shortcut the language you define
    (French = fr, English = en, Spanish = es, etc...)
    if not defined it will detect it or use english by default

    Example:
        >>> translate('hello there!', 'ru')
        Привет!
    """
    to_translate = urllib.quote_plus(text)
    link = URL % (to_lang, from_lang, to_translate)
    request = urllib2.Request(link, headers={'User-Agent': user_agent})
    raw_data = urllib2.urlopen(request).read()

    # data = raw_data.decode("utf-8")
    expr = r'class="t0">(.*?)<'
    re_result = re.findall(expr, raw_data)
    if len(re_result) == 0:
        result = ''
    else:
        resp_text = re_result[0].decode("utf-8")
        result = HTMLParser().unescape(resp_text)
    return result


def json_translate(text, to_lang='auto', from_lang='auto'):
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=2))
    session.mount('https://', HTTPAdapter(max_retries=2))

    params = {
        'client': 'gtx',
        'dt': 't',
        'sl': from_lang,
        'tl': to_lang,
        'q': text
    }
    request = requests.Request(
        method='GET',
        url=URL_JSON,
        headers={'User-Agent': user_agent},
        params=params)
    prepare = session.prepare_request(request)
    resp = session.send(prepare, verify=True)

    if resp.status_code != requests.codes.ok:
        resp.raise_for_status()

    json_fix = re.sub(r',+', ',', resp.content.decode('utf-8'))
    try:
        res = json.loads(json_fix)[0]
    except (ValueError, IndexError):
        return ''
    translations = map(lambda l: l[0], res)
    return ''.join(translations)


if __name__ == '__main__':

    tt = """
1. Links to FAQs in-app will use the encrypted app_id as we do now
2. App will register for encrypted app_id as it does now
3. In FB and WebC sends the URL will be `https:/my.website.com/{encrypted_appgroup_id}/faq/{faq_id}`
3a. The dl.agent.ai handler will redirect the {encrypted_appgroup_id} to HelpCenter based on {faq_id}
4. We will backlog a task for SDKs to support handlers for {encrypted_appgroup_id}
5. Over time we will deprecate app_id but there is a lot of backend code that deals with this and it would be a LOT of work to just remove it

This means:
a. No changes to SDKs needed immediately (just deals with {encryped_app_id})
b. Handler for deeplinks on the agent.ai server needs to support both {encrypted_app_id} and {encrypted_appgroup_id}
c. When client is Facebook or WebClient we should send links using the {encrypted_appgroup_id}
d. The Landing Page code will use the {encrypted_app_id}"""

    translate = json_translate

    for _ in range(10):
        print translate('hello there!', 'zh_cn')

    print translate('hello there!', 'ja')
    print translate('hello there!', 'ru')

    # for t in tt.split('\n'):
    print translate(tt, 'ru')
    # for _ in range(5): print translate(tt, 'ru')
