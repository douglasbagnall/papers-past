# -*- coding: utf-8 -*-
import unicodedata
import re

STX = '␂'
ETX = '␃'

# generated by caravel/corpus-utils, then modified by hand.
CHAR_MAP = {
    u'\n': u'\n',
    u' ': u' ',
    u'!': u'!',
    u'"': u'"',
    u'&': u'&',
    u"'": u"'",
    u'(': u'(',
    u')': u')',
    u'*': u'*',
    u',': u',',
    u'-': u'-',
    u'.': u'.',
    u'/': u'/',
    u'0': u'7',
    u'1': u'7',
    u'2': u'7',
    u'3': u'7',
    u'4': u'7',
    u'5': u'7',
    u'6': u'7',
    u'7': u'7',
    u'8': u'7',
    u'9': u'7',
    u':': u':',
    u';': u';',
    u'?': u'?',
    u'A': u'\xb9a',
    u'B': u'\xb9b',
    u'C': u'\xb9c',
    u'D': u'\xb9d',
    u'E': u'\xb9e',
    u'F': u'\xb9f',
    u'G': u'\xb9g',
    u'H': u'\xb9h',
    u'I': u'\xb9i',
    u'J': u'\xb9j',
    u'K': u'\xb9k',
    u'L': u'\xb9l',
    u'M': u'\xb9m',
    u'N': u'\xb9n',
    u'O': u'\xb9o',
    u'P': u'\xb9p',
    u'Q': u'\xb9q',
    u'R': u'\xb9r',
    u'S': u'\xb9s',
    u'T': u'\xb9t',
    u'U': u'\xb9u',
    u'V': u'\xb9v',
    u'W': u'\xb9w',
    u'X': u'\xb9x',
    u'Y': u'\xb9y',
    u'Z': u'\xb9z',
    u'[': u'(',
    u']': u')',
    u'a': u'a',
    u'b': u'b',
    u'c': u'c',
    u'd': u'd',
    u'e': u'e',
    u'f': u'f',
    u'g': u'g',
    u'h': u'h',
    u'i': u'i',
    u'j': u'j',
    u'k': u'k',
    u'l': u'l',
    u'm': u'm',
    u'n': u'n',
    u'o': u'o',
    u'p': u'p',
    u'q': u'q',
    u'r': u'r',
    u's': u's',
    u't': u't',
    u'u': u'u',
    u'v': u'v',
    u'w': u'w',
    u'x': u'x',
    u'y': u'y',
    u'z': u'z',
    u'{': u'(',
    u'\u03b1': u'a',       # "α" greek alpha
    u'}': u')',
    u'\xa3': u'\xa3',       # "£" -> "£"
    u'\xa5': u'¹y',         # "¥"
    u'\xdf': u'¹b',
    u'\u03b2': u'¹b',       # "β" greek
    u'\u03b3': u'y',       # "γ" -> "y" greek gamma
    u'\u2013': u'\u2014', #dashes
    u'\u2014': u'\u2014',
    u'…': u'...',
    u'×': u'x',
    u"“": u'"',
    u"”": u'"',
    u"‘": u"'",
    u"’": u"'",
    u"`": u"'",
    u"′": u"'",
    u'б': u'7',
    u'а': u'a',  # cyrillic a
    u'ƒ': u'f',
    u'\t': u' ',
    u'μ':  u'u',
}

NOISE_CHAR = u'°'

def normalise_text(raw_text, collapse_whitespace=0,
                   fix_soft_hyphens=False, fix_runs=3,
                   real_caps=False):
    m = CHAR_MAP.get
    noise = NOISE_CHAR
    if not isinstance(raw_text, unicode):
        raw_text = raw_text.decode('utf8')
    norm_text = unicodedata.normalize('NFKD', raw_text)
    utext = u''.join(m(x, noise) for x in norm_text)
    if real_caps:
        utext = re.sub(ur'¹\w', lambda x: x.group(0)[1].upper(), utext)
    text = utext.encode('utf-8').strip()
    if fix_soft_hyphens:
        # assume all double spaces are mis-processed soft-hyphens.
        text = text.replace('  ', '')
    if collapse_whitespace == 1:
        text = ' '.join(text.split())
    elif collapse_whitespace == 2:
        text = re.sub(r'[ \t]+', r' ', text)
    if fix_runs:
        text = re.sub(r'(\w)\1\1\1+', r'\1\1\1', text, flags=re.U)
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
