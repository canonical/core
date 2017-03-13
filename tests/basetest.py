import os
import shutil
import tempfile
import unittest


class HookTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        # mock systemctl as well as this is checked from the configure
        # hook and may not be available everyhwere
        self.mock_binary("systemctl", "")

    def mock_binary(self, basename, script):
        mocked_binary=os.path.join(self.tmp, basename)
        if not self.tmp in os.environ["PATH"]:
            os.environ["PATH"] = self.tmp+":"+os.environ["PATH"]
        with open(mocked_binary, "w") as fp:
            fp.write("#!/bin/sh\n%s\n" % script)
        os.chmod(mocked_binary, 0o755)

    def mock_snapctl(self, k, v):
        self.mock_binary("snapctl", """if [ "$1" = "get" ] && [ "$2" = "%s" ]; then echo "%s"; fi""" % (k, v))
