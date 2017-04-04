import plugin as p
import re

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
        if not self._pid:
            self.ignore()
            return

        self.ok('Community is OK')


