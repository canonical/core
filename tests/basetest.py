# Copyright (C) 2017 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
import tempfile
import unittest


class MockCmd:
    def __init__(self, tmpdir, basename, script):
        self.mocked_binary=os.path.join(tmpdir, basename)
        self.logfile = self.mocked_binary+".log"
        script="""#!/bin/sh
echo "$(basename "$0")" >> "{0}"
for arg in "$@"; do
    echo "$arg" >> "{0}"
done
echo >> "{0}"
{1}
        """.format(self.logfile, script)
        if not tmpdir in os.environ["PATH"]:
            os.environ["PATH"] = tmpdir+":"+os.environ["PATH"]
        with open(self.mocked_binary, "w") as fp:
            fp.write(script)
        os.chmod(self.mocked_binary, 0o755)
    def calls(self):
        with open(self.logfile) as fp:
            content = fp.read()
        all_calls = []
        for call in content.split("\n\n"):
            if call:
                all_calls.append(call.split("\n"))
        return all_calls


class HookTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        # mock systemctl as well as this is checked from the configure
        # hook and may not be available everyhwere
        self.mock_systemctl = self.mock_binary("systemctl", "")

    def mock_binary(self, basename, script):
        return MockCmd(self.tmp, basename, script)

    def mock_snapctl(self, k, v):
        self.mock_binary("snapctl", """if [ "$1" = "get" ] && [ "$2" = "%s" ]; then echo "%s"; fi""" % (k, v))
