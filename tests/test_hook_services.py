import subprocess

from .basetest import HookTest


class TestConfigureHookServices(HookTest):

    def test_configure_service_disable(self):
        self.mock_snapctl("service.ssh.disable", "true")
        subprocess.check_call(["hooks/configure"])

    def test_configure_service_enable(self):
        self.mock_snapctl("service.ssh.disable", "false")
        subprocess.check_call(["hooks/configure"])

    def test_configure_service_invalid(self):
        self.mock_snapctl("service.ssh.disable", "invalid")
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.check_call(["hooks/configure"], stderr=subprocess.DEVNULL)
        
