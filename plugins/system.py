import plugin as p
from include import compat as co
import re
import os

class SystemPlugin(p.Plugin):
    def checkSecurity(self, plugins_output):
        # SELinux
        if os.path.isfile('/sys/fs/selinux/enforce'):
            value = int(open('/sys/fs/selinux/enforce').readline())
            if not value:
                self.error('SELinux disabled')
            elif value == 1:
                self.ok('SELinux enabled in enforced mode')
            else:
                self.warning('SELinux mode unknown: %d', value)
        else:
            self.info('SELinux not installed')


    def checkAppArmor(self):
        result = os.popen('apparmor_status 2>/dev/null').read()
        lines = result.split('\n')
        mod_loaded = False
        enforce_mode = False
        for line in lines:
            if line.startswith('apparmor module is loaded'): mod_loaded = True
            if line.startswith('enforce mode'): enforce_mode = True

        if not mod_loaded:
            self.ok('AppArmor is not installed')
        elif enforce_mode:
            self.ok('AppArmor is enabled and in enforced mode')
        else:
            self.error('AppArmor is enabled but not in enforced mode')


    def checkIptables(self):
        result = os.popen('iptables -L 2>/dev/null').read()
        lines = result.split('\n')
        for line in lines:
            if 'REJECT' in line or 'DROP' in line:
                self.ok('iptables is enabled')
                return

        self.warning('iptables disabled')


