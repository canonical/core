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
        
