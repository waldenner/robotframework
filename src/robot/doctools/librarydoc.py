#  Copyright 2008-2012 Nokia Siemens Networks Oyj
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

import operator

from robot.utils import setter


class LibraryDoc(object):

    def __init__(self, name='', doc='', version='<unknown>', type='library',
                 scope='TEST CASE', named_args=False):
        self.name = name
        self.doc = doc
        self.version = version
        self.type = type
        self.scope = scope
        self.named_args = named_args
        self.inits = []
        self.keywords = []

    @setter
    def keywords(self, kws):
        return sorted(kws, key=operator.attrgetter('name'))


class KeywordDoc(object):

    def __init__(self, name='', args=None, doc=''):
        self.name = name
        self.args = args or []
        self.doc = doc

    @property
    def shortdoc(self):
        return self.doc.splitlines()[0] if self.doc else ''
