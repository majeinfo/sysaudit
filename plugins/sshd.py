import plugin as p
import re

class SshdPlugin(p.Plugin):
    def checkServerConf(self, plugins_output):
        with open('/etc/ssh/sshd_config') as f:
            for line in f:
                mobj = re.match('Protocol[ \t]+(.*)', line, re.IGNORECASE)
                if mobj:
                    sshd_versions = mobj.groups()[0].split(',')
                    if '1' in sshd_versions:
                        self.error('Protocol Version 1 should never be allowed')

                mob = re.match('PermitRootLogin[ \t]+yes', line, re.IGNORECASE)
                if mobj:
                    self.error("PermitRootLogin should be set to 'no'")

                mob = re.match('PasswordAuthentication[ \t]+yes', line, re.IGNORECASE)
                if mobj:
                    self.error("PasswordAuthentication should be set to 'no'")

