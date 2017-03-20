import plugin as p
from include import compat as co
import re

class SshdPlugin(p.Plugin):
    def checkServerConf(self, plugins_output):
        with open('/etc/ssh/sshd_config') as f:
            for line in f:
                mobj = re.match('Protocol[ \t]+(.*)', line, re.IGNORECASE)
                if mobj:
                    sshd_versions = mobj.groups()[0].split(',')
                    if '1' in sshd_versions:
                        co.display_test_error('Protocol Version 1 should never be allowed')

                mob = re.match('PermitRootLogin[ \t]+yes', line, re.IGNORECASE)
                if mobj:
                    co.display_test_error("PermitRootLogin should be set to 'no'")

                mob = re.match('PasswordAuthentication[ \t]+yes', line, re.IGNORECASE)
                if mobj:
                    co.display_test_error("PasswordAuthentication should be set to 'no'")

