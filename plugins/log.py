import plugin as p
from include import compat as co
from include import psutil as ps

class LogPlugin(p.Plugin):
    def checkDaemon(self, plugins_output):
        '''Check there is a log daemon running'''
        for pname in [ 'syslogd', 'rsyslogd', 'syslog-ng', 'systemd-journald' ]:
            pid = ps.check_process(pname)
            if pid:
                self.info('Log Process %s found' % pname)
                return

        self.error('No Process found for log processing')

    def checkLogrotate(self, plugins_output):
        '''Check if logrotate is installed and running.
           Also check that files under /var/log are managed
           by logrotate'''
        res = ps.managed_by_cron('logrotate')
        if not res:
            self.error('logrotate not called by cron job')
        else:
            self.info('logrotate called in cron file %s' % res[0])
