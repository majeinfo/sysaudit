import plugin as p
from include import compat as co
from include import fileutil as fu
import re
import os

MIN_PERCENT_FREE_BLOCKS = 20
MIN_PERCENT_FREE_INODES = 20

class FSPlugin(p.Plugin):
    def __init__(self):
        p.Plugin.__init__(self)
        self._mounts = self._get_mountpoints()  # { mount_point: { spec, fstype, options }, ... }
        self._swaps = self._get_swap_zones()
        self._mounted = self._get_mounted_fs()  # { mount_point: { spec, fstype, options }, ... }


    def check_etc_fstab(self):
        self._check_perms('/etc/fstab', {'owner': fu.MUST_BE_ROOT, 'group': fu.MUST_BE_ROOT, 'no_perms': fu.PERM_WRITE_OTHER })


    def check_mountpoints(self):
        '''Check if mount points are separated from /'''
        for d in ('/tmp', '/var', '/home'):
            if d not in self._mounts:
                self.warning('Directory %s should be a mount point' % d)


    def check_free_space(self):
        for mount_point, mount_def in self._mounted.items():
            stats = os.statvfs(mount_point)
            percent_bfree = (stats.f_bfree * 100.) / stats.f_blocks
            if percent_bfree < MIN_PERCENT_FREE_BLOCKS:
                self.warning('Filesystem %s has less then %d%% of free Blocks' % (MIN_PERCENT_FREE_BLOCKS, mount_def['spec']))


    def check_free_inodes(self):
        for mount_point, mount_def in self._mounted.items():
            stats = os.statvfs(mount_point)
            percent_bfree = (stats.f_ffree * 100.) / stats.f_files
            if percent_bfree < MIN_PERCENT_FREE_INODES:
                self.warning('Filesystem %s has less then %d%% of free Inodes' % (MIN_PERCENT_FREE_INODES, mount_def['spec']))


    def check_swap(self):
        if not len(self._swaps):
            self.warning('No Swap specified')


    def check_mount_options(self):
        '''noatime'''
        for mount_point, mount_def in self._mounts.items():
            if 'noatime' not in mount_def['options']:
                self.warning('Filesystem %s could be mounted with noatime option' % mount_def['spec'])


    def check_old_files(self):
        pass


    def check_lvm(self):
        pass


    def check_automount(self):
        for mount_point, mount_def in self._mounts.items():
            if (':' in mount_def['spec']) and ('nfs' in mount_def['fstype']):
                self.error('NFS %s should be auto-mounted and not listed in /etc/fstab' % mount_def['spec'])

            if ('//' in mount_def['spec']) and ('cifs' in mount_def['fstype'] or 'smb' in mount_def['fstype']):
                self.error('CIFS %s should be auto-mounted and not listed in /etc/fstab' % mount_def['spec'])


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


    def _get_mounted_fs(self):
        lines = open('/etc/mtab').readlines()
        mounted = {}
        for line in lines:
            parts = re.split('[ \t]+', line.strip())
            if len(parts) < 6: continue
            if parts[2] not in ('xfs', 'ext2', 'ext3', 'ext4', 'btrfs', 'zfs'): continue
            mounted[parts[1]] = { 'spec': parts[0], 'fstype': parts[2], 'options': parts[3] }

        return mounted
