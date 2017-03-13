import subprocess

from .basetest import HookTest


class TestConfigureHookServices(HookTest):

    def setUp(self):
        super(TestConfigureHookServices, self).setUp()
        
        self.mock_systemctl = self.mock_binary("systemctl", """
if [ "$1" = "is-enabled" ] && [ "$2" = "ssh.service" ]; then echo "disabled";exit 1; fi
if [ "$1" = "is-active" ] && [ "$2" = "ssh.service" ]; then echo "inactive";exit 1; fi
        """)

    
    def test_configure_service_disable(self):
        self.mock_snapctl("service.ssh.disable", "true")
        subprocess.check_call(["hooks/configure"])
        self.assertEqual(self.mock_systemctl.calls(), [
            ["systemctl", "--version"],
            ["systemctl", "disable", "ssh.service"],
            ["systemctl", "stop", "ssh.service"],
        ])

    def test_configure_service_enable(self):
        self.mock_snapctl("service.ssh.disable", "false")
        subprocess.check_call(["hooks/configure"])
        self.assertEqual(self.mock_systemctl.calls(), [
            ["systemctl", "--version"],
            ["systemctl", "is-enabled", "ssh.service"],
            ["systemctl", "enable", "ssh.service"],
            ["systemctl", "is-active", "ssh.service"],
            ["systemctl", "start", "ssh.service"],
        ])

    def test_configure_service_invalid(self):
        self.mock_snapctl("service.ssh.disable", "invalid")
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.check_call(["hooks/configure"], stderr=subprocess.DEVNULL)
        
