# -*- coding: utf-8 -*-
import unicodedata
import re

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

def normalise_text(raw_text, collapse_whitespace=0,
                   collapse_digits=False, fix_soft_hyphens=False):
    m = CHAR_MAP.get
    noise = NOISE_CHAR
    if not isinstance(raw_text, unicode):
        raw_text = raw_text.decode('utf8')
    norm_text = unicodedata.normalize('NFKD', raw_text)
    utext = u''.join(m(x, noise) for x in norm_text)
    text = utext.encode('utf-8').strip()
    if fix_soft_hyphens:
        # assume all double spaces are mis-processed soft-hyphens.
        text = text.replace('  ', '')
    if collapse_whitespace == 1:
        text = ' '.join(text.split())
    elif collapse_whitespace == 2:
        text = re.sub(r'  +', r'  ', text)
    if collapse_digits:
        text = re.sub(r'[0-9]', '7', text)
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
