import plugin as p
from include import compat as co
from include import fileutil as fu
import pwd, spwd

class PasswordPlugin(p.Plugin):
    def check_files(self, plugins_output):
        self._check_perms('/etc/passwd', { 'owner': fu.MUST_BE_ROOT, 'group': fu.MUST_BE_ROOT, 'no_perms': fu.PERM_WRITE_OTHER })
        self._check_perms('/etc/shadow', {'owner': fu.MUST_BE_ROOT, 'group': fu.MUST_BE_ROOT, 'no_perms': fu.PERM_ANY_OTHER })
        self._check_perms('/etc/group', {'owner': fu.MUST_BE_ROOT, 'group': fu.MUST_BE_ROOT, 'no_perms': fu.PERM_WRITE_OTHER })

    def check_empty_password(self, plugins_output):
        for (pw_name, _, pw_uid, pw_gid, _, _, pw_shell) in pwd.getpwall():
            (_, sp_pwd, _, _, _, _, _, _, _) = spwd.getspnam(pw_name)
            if sp_pwd == '':
                self.error('User %s has an empty password' % pw_name)

    def check_password_policy(self):
        # TODO: check password policy
        pass
