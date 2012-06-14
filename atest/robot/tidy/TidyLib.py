from __future__ import with_statement

import os
from os.path import abspath, dirname, join
from subprocess import call, STDOUT
import tempfile

from robot.utils.asserts import assert_equals

ROBOT_SRC = join(dirname(abspath(__file__)), '..', '..', '..', 'src')


class TidyLib(object):

    def __init__(self, interpreter):
        self._cmd = [interpreter, '-m', 'robot.tidy']
        self._interpreter = interpreter

    def run_tidy_and_return_output(self, options, input, command=None):
        """Runs tidy in the operating system and returns output."""
        options = options.split(' ') if options else []
        with tempfile.TemporaryFile() as output:
            rc = call(self._cmd + options + [self._path(input)], stdout=output,
                      stderr=STDOUT, cwd=ROBOT_SRC, shell=os.sep=='\\')
            output.seek(0)
            content = output.read()
            if rc:
                raise RuntimeError(content)
            return content

    def run_tidy_and_check_result(self, options, input, expected):
        """Runs tidy and checks that output matches content of file `expected`."""
        result = self.run_tidy_and_return_output(options, input)
        self._assert_result(result, open(self._path(expected)).read())

    def run_tidy_as_a_script_and_check_result(self, options, input, expected):
        """Runs tidy and checks that output matches content of file `expected`."""
        cmd = [self._interpreter, join(ROBOT_SRC, 'robot', 'tidy.py')]
        result = self.run_tidy_and_return_output(options, input, cmd)
        self._assert_result(result, open(self._path(expected)).read())

    def _path(self, path):
        return path.replace('/', os.sep)

    def _assert_result(self, result, expected):
        result = result.decode('UTF-8')
        expected = expected.decode('UTF-8')
        result_lines = result.splitlines()
        expected_lines = expected.splitlines()
        for line1, line2 in zip(result_lines, expected_lines):
            msg = "\n%s\n!=\n%s\n" % (result, expected)
            assert_equals(repr(unicode(line1)), repr(unicode(line2)), msg)
