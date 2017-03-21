import os
from include import compat as co

MUST_BE_ROOT = 'must_root'
MUST_NOT_BE_ROOT =  'must_not_root'

PERM_READ_OTHER = 4
PERM_WRITE_OTHER = 2
PERM_EXECUTE_OTHER = 1
PERM_ANY_OTHER = 7
PERM_READ_GROUP = 4 << 3
PERM_WRITE_GROUP = 2 << 3
PERM_EXECUTE_GROUP = 1 << 3
PERM_ANY_GROUP = 7 << 3
PERM_READ_USER = 4 << 6
PERM_WRITE_USER = 2 << 6
PERM_EXECUTE_USER = 1 << 6
PERM_ANY_USER = 7 << 6
PERM_SETUIDBIT = 4 << 9
PERM_SETGIDBIT = 2 << 9
PERM_STICKYBIT = 1 << 9

MSG_OK = 0
MSG_INFO = 1
MSG_WARN = 2
MSG_ERR = 3

class Plugin(object):
    def __init__(self):
        co.debug('Plugin run')
        self.output = {}

    def begin(self, func_name):
        self.errors = 0
        self.msgs = []
        co.begin_test('Execute: ' + func_name)

    def ok(self, msg=''):
        self.msgs.append((MSG_OK, msg))

    def info(self, msg):
        self.msgs.append((MSG_INFO, msg))

    def warning(self, msg):
        self.msgs.append((MSG_WARN, msg))

    def error(self, msg):
        self.errors += 1
        self.msgs.append((MSG_ERR, msg))

    def end(self):
        # Compute the final result
        if not self.errors:
            co.end_test_ok()
        else:
            co.end_test_failed()

        for level, msg in self.msgs:
            if level == MSG_OK: co.display_ok(msg)
            elif level == MSG_INFO: co.display_info(msg)
            elif level == MSG_WARN: co.display_warning(msg)
            elif level == MSG_ERR: co.display_err(msg)
            else: co.display_err('UNKNOWN MSG LEVEL')


    def _check_perms(self, filename, attrs):
        '''Check filename towards owner, group and perms given in attrs dictionary.'''
        self.info('check_perms(%s)' % filename)
        if not os.path.exists(filename):
            self.error('File %s does not exist' % filename)
            return

        try:
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filename)
            mode = mode & ~(-1 << 12)

            if 'owner' in attrs:
                if type(attrs['owner']) == str:
                    if attrs['owner'] == MUST_BE_ROOT and uid != 0:
                        self.error('Owner mismatch: wanted %s, got %d' % (attrs['owner'], uid))
                    elif attrs['owner'] == MUST_NOT_BE_ROOT and uid == 0:
                        self.error('Owner mismatch: wanted %s, got %d' % (attrs['owner'], uid))
                elif attrs['owner'] != uid:
                    self.error('Owner mismatch: wanted %d, got %d' % (attrs['owner'], uid))

            if 'no_perms' in attrs:
                if mode & attrs['no_perms']:
                    self.error('Perms mismatch: %o perms must be excluded, but perms %o found' % (attrs['no_perms'], mode))

            if 'perms' in attrs:
                if not (mode & attrs['perms']):
                    self.error('Perms mismatch: %o perms must be included, but perms %o found' % (attrs['perms'], mode))

        except Exception as exc:
            self.error('check_perms failed: %s' % exc)


    def _get_kernel_parm(self, name):
        '''Read the given kernel parameter value, from /proc/sys.

        Parameter name form is : xxx.yyy.zzz
        '''
        try:
            fname = name.replace('.', '/')
            with open('/proc/sys/' + fname) as f:
                return f.readline().strip()
        except:
            self.info('Kernel Parameter %s not found' % name)

        return None


    def _check_kernel_parm(self, name, expected_value):
        '''Check the kernel parameter value'''
        self.info('check_kernel_parm(%s=%d)' % (name, expected_value))
        value = self._get_kernel_parm(name)
        if not value:
            return None

        if int(value) != expected_value:
            self.error("Kernel Parameter '%s' value should be %d instead of %d" % (name, expected_value, int(value)))
            return False

        return True
