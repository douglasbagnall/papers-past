# -*- coding: utf-8 -*-
import unicodedata

STX = '␂'
ETX = '␃'


def _make_char_map():
    chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                '0123456789!"$%&()*,-./:;?\n \'—£'.decode('utf8'))
    map_chars = {
        'б': '6',
        'а': 'a',  # cyrllic a is surprisingly common
        'ƒ': 'f',
        '\t': ' ',
        'μ':  'u',
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "`": "'",
        "′": "'",
        '–': '—',
        '…': '...',
        '[': '(',
        ']': ')',
        '×': 'x',
    }
    char_map = {k.decode('utf8'): v.decode('utf8')
                for k, v in map_chars.items()}
    char_map.update({x: x for x in chars})
    return char_map

CHAR_MAP = _make_char_map()
NOISE_CHAR = '°'.decode('utf-8')


def normalise_text(raw_text, stxetx=False, collapse_whitespace=False):
    m = CHAR_MAP.get
    noise = NOISE_CHAR
    if not isinstance(raw_text, unicode):
        raw_text = raw_text.decode('utf8')
    nfd_text = unicodedata.normalize('NFD', raw_text)
    utext = u''.join(m(x, noise) for x in nfd_text)
    text = utext.encode('utf-8').strip()
    if collapse_whitespace:
        text = ' '.join(text.split())
    if stxetx:
        return '␂%s␃' % text
    return text


BOOK_HEADERS = set(("title", "author", "date", "id", "type"))

ARTICLE_HEADERS = set(("title", "url", "issue-title", "issue-code",
                       "type", "id"))

ALL_HEADERS = BOOK_HEADERS | ARTICLE_HEADERS


def read_header(f, keys=ALL_HEADERS):
    headers = {}
    n_bytes = 0
    for line in f:
        n_bytes += len(line)
        line = line.strip()
        if not line:
            break
        k, v = line.split(':', 1)
        k = k.lower().replace('\xef\xbb\xbf', '')
        if k not in keys:
            raise ValueError("'%s' is not a valid header" % k)
        headers[k] = v.strip()

    return headers, n_bytes
