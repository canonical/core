import os
import unittest


class ConfigureTestCase(unittest.TestCase):

    def mock_binary(self, basename, script):
        mocked_binary=os.path.join(self.tmp, basename)
        if not self.tmp in os.environ["PATH"]:
            os.environ["PATH"] = self.tmp+":"+os.environ["PATH"]
        with open(mocked_binary, "w") as fp:
            fp.write("#!/bin/sh\n%s\n" % script)
        os.chmod(mocked_binary, 0o755)

    def mock_snapctl(self, k, v):
        self.mock_binary("snapctl", """if [ "$1" = "get" ] && [ "$2" = "%s" ]; then echo "%s"; fi""" % (k, v))

    

