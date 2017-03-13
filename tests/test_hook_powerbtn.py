import os
import subprocess

from .basetest import HookTest


class TestConfigurePowerkey(HookTest):

    def test_configure_powerkey(self):
        os.environ["TEST_LOGIN_CONF_D"]=self.tmp
        self.mock_snapctl("system.power-key-action", "ignore")
        subprocess.check_call(["hooks/configure"])

    def test_configure_powerkey_invalid(self):
        self.mock_snapctl("system.power-key-action", "invalid")
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.check_call(["hooks/configure"], stderr=subprocess.DEVNULL)
        
