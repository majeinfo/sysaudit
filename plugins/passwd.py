import plugin as p
from include import compat as co
from include import fileutil as fu
import pwd, spwd

class PasswordPlugin(p.Plugin):
    # TODO: check account without password
    # TODO: check password policy

    def check_files(self, plugins_output):
        fu.check_perms('/etc/passwd', { 'owner': fu.MUST_BE_ROOT, 'group': fu.MUST_BE_ROOT, 'no_perms': fu.PERM_WRITE_OTHER })
        fu.check_perms('/etc/shadow', {'owner': fu.MUST_BE_ROOT, 'group': fu.MUST_BE_ROOT, 'no_perms': fu.PERM_ANY_OTHER })
        fu.check_perms('/etc/group', {'owner': fu.MUST_BE_ROOT, 'group': fu.MUST_BE_ROOT, 'no_perms': fu.PERM_WRITE_OTHER })

    def check_empty_password(selfself, plugins_output):
        for (pw_name, _, pw_uid, pw_gid, _, _, pw_shell) in pwd.getpwall():
            (_, sp_pwd, _, _, _, _, _, _, _) = spwd.getspnam(pw_name)
            if sp_pwd == '':
                co.display_test_error('User %s has an empty password' % pw_name)


