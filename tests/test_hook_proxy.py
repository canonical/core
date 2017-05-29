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
import subprocess
import tempfile

from .test_configure import ConfigureTestCase

mock_etc_environment = """PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
"""

class TestConfigureHookProxy(ConfigureTestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)

    def mock_etc_environment(self, txt):
        self.mock_etc_environment_path = os.path.join(self.tmp, "environment")
        with open(self.mock_etc_environment_path, "w") as fp:
            fp.write(txt)
        os.environ["TEST_ETC_ENVIRONMENT"]=self.mock_etc_environment_path

    def read_mock_etc_environment(self):
        with open(self.mock_etc_environment_path) as fp:
            content=fp.read()
        return content

    def test_configure_proxy_adds_new(self):
        self.mock_etc_environment(mock_etc_environment)
        self.mock_snapctl("proxy.http", "http://bar.com")
        
        subprocess.check_call(["hooks/configure"])

        expected=mock_etc_environment+"http_proxy=http://bar.com\n"
        self.assertEqual(self.read_mock_etc_environment(), expected)

    def test_configure_proxy_replace_existing(self):
        self.mock_etc_environment(mock_etc_environment+"http_proxy=http://foo.com")
        self.mock_snapctl("proxy.http", "http://bar.com")
        
        subprocess.check_call(["hooks/configure"])

        expected=mock_etc_environment+"http_proxy=http://bar.com\n"
        self.assertEqual(self.read_mock_etc_environment(), expected)

    def test_configure_proxy_removes_existing(self):
        self.mock_etc_environment(mock_etc_environment+"http_proxy=http://foo.com")
        self.mock_snapctl("proxy.http", "")
        
        subprocess.check_call(["hooks/configure"])

        expected=mock_etc_environment
        self.assertEqual(self.read_mock_etc_environment(), expected)

    def test_configure_proxy_replaces_with_ro_directory(self):
        self.mock_etc_environment(mock_etc_environment+"http_proxy=some")
        self.mock_snapctl("proxy.http", "http://bar.com")
        # simulate that bits of the dir are not writable
        with open(self.mock_etc_environment_path+".tmp", "w"):
            pass
        os.chmod(self.mock_etc_environment_path+".tmp", 0o555)
        
        subprocess.check_call(["hooks/configure"])

        expected=mock_etc_environment+"http_proxy=http://bar.com\n"
        self.assertEqual(self.read_mock_etc_environment(), expected)

    def test_configure_proxy_removes_with_ro_directory(self):
        self.mock_etc_environment(mock_etc_environment+"http_proxy=some")
        self.mock_snapctl("proxy.http", "")
        # simulate that bits of the dir are not writable
        with open(self.mock_etc_environment_path+".tmp", "w"):
            pass
        os.chmod(self.mock_etc_environment_path+".tmp", 0o555)
        
        subprocess.check_call(["hooks/configure"])

        expected=mock_etc_environment
        self.assertEqual(self.read_mock_etc_environment(), expected)

    def test_configure_proxy_no_change_unset(self):
        self.mock_etc_environment(mock_etc_environment)
        st1 = os.stat(self.mock_etc_environment_path)
        self.mock_snapctl("proxy.http", "")
        subprocess.check_call(["hooks/configure"])
        st2 = os.stat(self.mock_etc_environment_path)
        self.assertEqual(st1.st_mtime_ns, st2.st_mtime_ns)

    def test_configure_proxy_no_change_set(self):
        self.mock_etc_environment(mock_etc_environment+"http_proxy=http://foo.com")
        st1 = os.stat(self.mock_etc_environment_path)
        self.mock_snapctl("proxy.http", "http://foo.com")
        subprocess.check_call(["hooks/configure"])
        st2 = os.stat(self.mock_etc_environment_path)
        self.assertEqual(st1.st_mtime_ns, st2.st_mtime_ns)

    def test_configure_proxy_adds_new_all_supported_proxies(self):
        for proto in ["http", "https", "ftp", "all"]:
            self.mock_etc_environment(mock_etc_environment)
            self.mock_snapctl("proxy.{}".format(proto), "{}://bar.com".format(proto))
            subprocess.check_call(["hooks/configure"])

            expected=mock_etc_environment+"{}_proxy={}://bar.com\n".format(proto, proto)
            self.assertEqual(self.read_mock_etc_environment(), expected)
