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
import subprocess

from .basetest import HookTest


class TestConfigurePowerkey(HookTest):

    def test_configure_powerkey(self):
        os.environ["TEST_LOGIN_CONF_D"]=self.tmp
        self.mock_snapctl("system.power-key-action", "ignore")
        subprocess.check_call(["hooks/configure"])
        with open(os.path.join(self.tmp, "00-snap-core.conf")) as fp:
            content=fp.read()
        self.assertEqual(content, """[Login]
HandlePowerKey=ignore
""")

    def test_configure_powerkey_invalid(self):
        self.mock_snapctl("system.power-key-action", "invalid")
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.check_call(["hooks/configure"], stderr=subprocess.DEVNULL)
        
