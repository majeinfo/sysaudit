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

        #TODO: AppArmor
        #TODO: iptables
