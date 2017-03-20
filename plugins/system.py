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
                co.display_test_error('SELinux disabled')
            elif value == 1:
                co.display_test_ok('SELinux enabled in enforced mode')
            else:
                co.display('SELinux mode unknown: %d', value)
        else:
            co.display('SELinux not installed')

        #TODO: AppArmor
