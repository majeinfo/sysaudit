'''Useful functions to handle process management'''
import os
import re
import glob
from include import compat as co

def check_process(process_name, multi=False):
    '''Returns the PID of the specified process or False if not found.
       In case of multiple processes, returns only the 1st PID'''
    # TODO: add a flag for multiple PID
    try:
        procs = os.popen("ps -e | grep -i '%s' | grep -v grep" % process_name).read()
        lines = procs.strip().split('\n')
        if len(lines) < 1: return False
        for line in lines:
            if not line: continue
            cols = re.split('[ \t]+', line.strip())
            if len(cols) and cols[3] == process_name:
                return int(cols[0])      # return PID
    except Exception as exc:
        co.display_err('os.popen failed: %s' % exc)

    return False

def managed_by_cron(process_name, is_system=True):
    '''Returns a tuple with the filename and the command
       that launches the specified process from crontab.
       Returns () in not found'''
    pat = re.compile(process_name)

    def _search(name, re_process):
        '''Search pe_process in name file or name directory'''
        if os.path.isdir(name):
            for f in glob.glob(name + '/*'):
                res = _search(f, re_process)
                if res: return res

        # Search in a file
        if not os.path.isfile(name):
            return ()

        with open(name) as f:
            for line in f:
                if pat.search(line): return (name, re_process)

        return ()

    names = ('/etc/crontab', '/etc/cron.d', '/etc/cron.hourly', '/etc/cron.daily', '/etc/cron.weekly', '/etc/cron.monthly')
    for n in names:
        res = _search(n, process_name)
        if res: return res

    return ()
