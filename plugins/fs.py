import plugin as p
from include import compat as co
from include import fileutil as fu
import re

class FSPlugin(p.Plugin):
    def __init__(self):
        p.Plugin.__init__(self)
        self._mounts = self._get_mountpoints()  # { mount_point: { spec, fstype, options }, ... }


    def check_etc_fstab(self):
        self._check_perms('/etc/fstab', {'owner': fu.MUST_BE_ROOT, 'group': fu.MUST_BE_ROOT, 'no_perms': fu.PERM_WRITE_OTHER })

        for mount_point, mount_def in self._mounts.items():
            if (':' in mount_def['spec']) and ('nfs' in mount_def['fstype']):
                self.error('NFS %s should be auto-mounted and not listed in /etc/fstab' % mount_def['spec'])

            if ('//' in mount_def['spec']) and ('cifs' in mount_def['fstype'] or 'smb' in mount_def['fstype']):
                self.error('CIFS %s should be auto-mounted and not listed in /etc/fstab' % mount_def['spec'])


    def check_mountpoints(self):
        '''Check if mount points are separated from /'''
        mounts = self._get_mountpoints()
        for d in ('/tmp', '/var', '/home'):
            if d not in mounts:
                self.warning('Directory %s should be a mount point' % d)


    def check_free_space(self):
        pass


    def check_free_inodes(self):
        pass


    def check_swap(self):
        swaps = self._get_swap_zones()
        if not len(swaps):
            self.warning('No Swap specified')


    def check_mount_options(self):
        '''noatime'''
        for mount_point, mount_def in self._get_mountpoints().items():
            if 'noatime' not in mount_def['options']:
                self.warning('Filesystem %s could be mounted with noatime option' % mount_def['spec'])


    def check_old_files(self):
        pass


    def check_lvm(self):
        pass


    def check_automount(self):
        pass


    def _get_mountpoints(self):
        lines = open('/etc/fstab').readlines()
        mounts = {}
        for line in lines:
            if line[0] == '#': continue
            parts = re.split('[ \t]+', line.strip())
            if len(parts) < 6: continue
            if parts[2] == 'swap': continue
            mounts[parts[1]] = { 'spec': parts[0], 'fstype': parts[2], 'options': parts[3]}

        return mounts


    def _get_swap_zones(self):
        swaps = open('/proc/swaps').readlines()[1:]
        return swaps

