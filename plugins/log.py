import re
import os
import plugin as p

LOG_PROCESS = 'log_process'
LOG_SERVER = 'log_server'

class LogPlugin(p.Plugin):
    def checkDaemon(self, plugins_output):
        '''Check there is a log daemon running'''
        for pname in [ 'syslogd', 'rsyslogd', 'syslog-ng', 'systemd-journald' ]:
            pid = self._check_process(pname)
            if pid:
                self.info('Log Process %s found' % pname)
                self.output[LOG_PROCESS] = pname
                return

        self.error('No Process found for log processing')


    def checkLogrotate(self, plugins_output):
        '''Check if logrotate is installed and running.
           Also check that files under /var/log are managed
           by logrotate'''
        res = self._managed_by_cron('logrotate')
        if not res:
            self.error('logrotate not called by cron job')
        else:
            self.info('logrotate called in cron file %s' % res[0])


    def check_log_server(self):
        '''Check if the logs are redirected to a log server'''
        # configuration depends on log process
        if self.output[LOG_PROCESS] == 'rsyslogd':
            for f in [ '/etc/rsyslog.conf', '/etc/rsyslog.d/rsyslog.conf' ]:
                if os.path.isfile(f):
                    conf_file = f
                    break
            else:
                self.warning('Configuration file for rsyslogd not found')
                return

            with open(conf_file) as f:
                for line in f:
                    mobj = re.match('[^#].*@+([^:]+)', line, re.IGNORECASE)
                    if mobj:
                        self.output[LOG_SERVER] = mobj.groups()[0]
                        self.info('Log Server found: %s' % self.output[LOG_SERVER])
                        return
            return

        self.warning('Cannot determine if a Log Server has been configured')



