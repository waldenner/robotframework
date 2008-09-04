#  Copyright 2008 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import re
import string

from robottypes import is_str, is_list, is_tuple


_escape_re = re.compile(r'(\\+)([^\\]{,2})')   # escapes and nextchars


def escape(item):
    if not is_str(item):
        return item
    for orig in [ '\\', '${', '@{', '%{', '&{', '*{' ]:
        item = item.replace(orig, '\\' + orig)
    return item

def unescape(item):
    if not is_str(item):
        return item
    result = []
    unprocessed = item
    while True:
        res = _escape_re.search(unprocessed)
        # If no escapes found append string to result and exit loop
        if res is None:
            result.append(unprocessed)
            break
        # Split string to pre match, escapes, nextchars and unprocessed parts
        # (e.g. '<pre><esc><nc><unproc>') where nextchars contains 0-2 chars
        # and unprocessed may contain more escapes. Pre match part contains
        # no escapes can is appended directly to result.
        result.append(unprocessed[:res.start()])
        escapes = res.group(1)
        nextchars = res.group(2)
        unprocessed = unprocessed[res.end():]
        # Append every second escape char to result
        result.append('\\' * (len(escapes) / 2))
        # Handle '\n', '\r' and '\t'. Note that both '\n' and '\n ' are 
        # converted to '\n'
        if len(escapes) % 2 == 0 or len(nextchars) == 0 \
                    or nextchars[0] not in ['n','r','t']:
            result.append(nextchars)
        elif nextchars[0] == 'n':
            if len(nextchars) == 1 or nextchars[1] == ' ':
                result.append('\n')
            else:
                result.append('\n' + nextchars[1])
        elif nextchars[0] == 'r':
            result.append('\r' + nextchars[1:])
        else:
            result.append('\t' + nextchars[1:])
    return ''.join(result)


def escape_file_name(filename):
    """Escapes filename. 
    
    Use only with actual file name and not with full path because possible
    '/' and '\\' in the given name are also escaped!
    """
    return ''.join([ _escape_char(c) for c in filename ])        


_ok_chars = string.ascii_letters + string.digits + '-+.'
_replaced_chars = { u'\xe4' : 'a',  u'\xe5' : 'a',
                    u'\xc4' : 'A',  u'\xc5' : 'A',
                    u'\xf6' : 'o',  u'\xd6' : 'O',
                    u'\xfc' : 'u',  u'\xdc' : 'U', }

def _escape_char(char):
    if char in _ok_chars:  
        return char
    elif _replaced_chars.has_key(char):
        return _replaced_chars[char]
    else:
        return '_'
    