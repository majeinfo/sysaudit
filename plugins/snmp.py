import plugin as p
import re
import os

class SnmpPlugin(p.Plugin):
    def __init__(self):
        p.Plugin.__init__(self)
        self._pid = self._check_process('snmpd')


    def checkRunning(self):
        if not self._pid:
            self.ok('snmpd daemon not running')
        else:
            self.info('snmpd daemon is running')


    def checkCommunity(self):
        # Test the config file instead of calling snmpd Agent

        #if not self._pid:
        #    self.ignore()
        #    return

        if not os.path.exists('/etc/snmp/snmpd.conf'):
            self.ok('snmpd configuration not found')
            return

        with open('/etc/snmp/snmpd.conf') as f:
            for line in f:
                line = line.strip()
                mobj = re.match('rocommunity[ \t]+public[ \t]+', line, re.IGNORECASE)
                if mobj:
                    self.warning("rocommunity 'public' found")
                mobj = re.match('rwcommunity[ \t]+private[ \t]+', line, re.IGNORECASE)
                if mobj:
                    self.error("rwcommunity 'private' found")

                mobj = re.match('authcommunity[ \t]+public[ \t]+', line, re.IGNORECASE)
                if mobj:
                    self.warning("authcommunity 'public' found")
                mobj = re.match('authcommunity[ \t]+private[ \t]+', line, re.IGNORECASE)
                if mobj:
                    self.error("authcommunity 'private' found")

                mobj = re.match('com2sec[ \t]+.*[ \t]+([^ \t]+)', line, re.IGNORECASE)
                if mobj:
                    community = mobj.groups()[0]
                    if community == 'public' or community == 'private':
                        self.error("com2sec found with community " + community)


