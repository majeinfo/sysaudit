import plugin as p
from include import compat as co
from include import fileutil as fu

class PermissionsPlugin(p.Plugin):
    # TODO: check account without password
    # TODO: check password policy

    def check_dirs(self, plugins_output):
        fu.check_perms('/root', { 'owner': fu.MUST_BE_ROOT, 'group': fu.MUST_BE_ROOT, 'no_perms': fu.PERM_ANY_OTHER|fu.PERM_ANY_GROUP })

        for dirname in [ '/bin', '/sbin', '/lib', '/etc', '/var', '/usr',
                         '/usr/bin', '/usr/sbin', '/usr/lib', '/usr/local',
                         '/usr/local/bin', '/usr/local/sbin', '/usr/local/lib', '/usr/local/etc',
                         '/var/log', '/var/lib', '/var/spool' ]:
            fu.check_perms(dirname, { 'owner': fu.MUST_BE_ROOT, 'group': fu.MUST_BE_ROOT, 'no_perms': fu.PERM_WRITE_OTHER })

        fu.check_perms('/tmp', { 'owner': fu.MUST_BE_ROOT, 'group': fu.MUST_BE_ROOT, 'perms': fu.PERM_STICKYBIT })

    def check_files(self, plugins_output):
        pass



