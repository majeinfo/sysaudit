import plugin as p
from include import compat as co
from include import fileutil as fu
import re

class FSPlugin(p.Plugin):
    def check_etc_fstab(self, plugins_output):
        fu.check_perms('/etc/fstab', {'owner': fu.MUST_BE_ROOT, 'group': fu.MUST_BE_ROOT, 'no_perms': fu.PERM_WRITE_OTHER })

        with open('/etc/fstab') as f:
            for line in f:
                if line[0] == '#': continue
                cols = re.split('[ \t]+', line)
                if len(cols) < 6: continue

                if (':' in cols[1]) and ('nfs' in cols[2]):
                    co.display_test_error('NFS %s should be auto-mounted and not listed in /etc/fstab' % cols[1])

                if '//' in cols[1] and ('cifs' in cols[2] or 'smb' in cols[2]):
                    co.display_test_error('CIFS %s should be auto-mounted and not listed in /etc/fstab' % cols[1])
