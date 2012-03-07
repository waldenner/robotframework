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

from contextlib import contextmanager
import os.path

from robot.utils import timestamp_to_secs, get_link_path, html_format

from .stringcache import StringCache


class JsBuildingContext(object):

    def __init__(self, log_path=None, split_log=False, prune_input=False):
        # log_path can be a custom object in unit tests
        self._log_dir = os.path.dirname(log_path) \
                if isinstance(log_path, basestring) else None
        self._split_log = split_log
        self._prune_input = prune_input
        self._strings = self._orig_strings = StringCache()
        self.basemillis = None
        self.split_results = []
        self._msg_links = {}

    def string(self, string):
        return self._strings.add(string)

    def html(self, string):
        return self.string(html_format(string))

    def relative_source(self, source):
        rel_source = get_link_path(source, self._log_dir) \
            if self._log_dir and source and os.path.exists(source) else ''
        return self.string(rel_source)

    def timestamp(self, time):
        if not time:
            return None
        # Must use `long` due to http://ironpython.codeplex.com/workitem/31549
        millis = long(round(timestamp_to_secs(time) * 1000))
        if self.basemillis is None:
            self.basemillis = millis
        return millis - self.basemillis

    def create_link_target(self, msg):
        self._msg_links[self._link_key(msg)] = self.string(msg.parent.id)

    def _link_key(self, msg):
        return (msg.message, msg.level, msg.timestamp)

    def link(self, msg):
        return self._msg_links.get(self._link_key(msg))

    @property
    def strings(self):
        return self._strings.dump()

    def start_splitting_if_needed(self, split=False):
        if self._split_log and split:
            self._strings = StringCache()
            return True
        return False

    def end_splitting(self, model):
        self.split_results.append((model, self.strings))
        self._strings = self._orig_strings
        return len(self.split_results)

    @contextmanager
    def prune_input(self, *items):
        yield
        if self._prune_input:
            for item in items:
                item.clear()
