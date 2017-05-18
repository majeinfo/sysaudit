import plugin as p
import socket
import re

class NetworkPlugin(p.Plugin):
    def __init__(self):
        p.Plugin.__init__(self)
        self.output['time_server'] = []


    def checkObsoleteService(self):
        protos = { 'telnet': 23, 'rexec': 512, 'rlogin': 513, 'rsh': 514, 'printer': 515 }

        for proto, port in protos.items():
            try:
                sock = socket.create_connection(('127.0.0.1', port), timeout=1)
                sock.close()
                self.error('Protocol ' + proto + ' is enabled on port ' + str(port))
            except:
                pass


    def checkTimeSynchro(self):
        # ntpd or chronyd ?
        ntpd = self._check_process('ntpd')
        chronyd = self._check_process('chronyd')
        if not ntpd and not chronyd:
            self.error('Neither ntpd or chronyd started')
            return

        if ntpd: conf_name = '/etc/ntp.conf'
        elif chronyd: conf_name = '/etc/chrony.conf'

        with open(conf_name) as f:
            for line in f:
                mobj = re.match('server[ \t]+([^ \t]+)', line, re.IGNORECASE)
                if mobj: self.output['time_server'].append(mobj.groups()[0])
