import plugin as p
import re

class DNSClientPlugin(p.Plugin):
    def __init__(self):
        p.Plugin.__init__(self)
        self.dns_server = []
        self.dns_domain = None
        self.dns_search = []

    def checkClientConf(self, plugins_output):
        with open('/etc/resolv.conf') as f:
            for line in f:
                mobj = re.match('nameserver[ \t]+(.*)', line, re.IGNORECASE)
                if mobj:
                    self.dns_server.append(mobj.groups()[0])
                    self.output['dns_server'] = mobj.groups()[0]

                mobj = re.match('domain[ \t]+(.*)', line, re.IGNORECASE)
                if mobj:
                    self.dns_domain = mobj.groups()[0]
                    self.output['dns_domain'] = mobj.groups()[0]

                mobj = re.match('search[ \t]+(.*)', line, re.IGNORECASE)
                if mobj:
                    self.dns_search = re.split('[ \t]+', mobj.groups()[0])
                    self.output['dsn_search'] = re.split('[ \t]+', mobj.groups()[0])



