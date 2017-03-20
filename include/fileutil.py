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

# TODO: write a function that convert octal to symbolic perms

def check_perms(filename, attrs):
    '''Check filename towards owner, group and perms given in attrs dictionary.'''
    co.display_begin_test('check_perms(%s)' % filename)
    if not os.path.exists(filename):
        co.display_test_error('File %s does not exist' % filename)
        return

    try:
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filename)
        mode = mode & ~(-1 << 12)

        if 'owner' in attrs:
            if type(attrs['owner']) == str:
                if attrs['owner'] == MUST_BE_ROOT and uid != 0:
                    co.display_test_error('Owner mismatch: wanted %s, got %d' % (attrs['owner'], uid))
                elif attrs['owner'] == MUST_NOT_BE_ROOT and uid == 0:
                    co.display_test_error('Owner mismatch: wanted %s, got %d' % (attrs['owner'], uid))
            elif attrs['owner'] != uid:
                co.display_test_error('Owner mismatch: wanted %d, got %d' % (attrs['owner'], uid))

        if 'no_perms' in attrs:
            if mode & attrs['no_perms']:
                co.display_test_error('Perms mismatch: %o perms must be excluded, but perms %o found' % (attrs['no_perms'], mode))

        if 'perms' in attrs:
            if not (mode & attrs['perms']):
                co.display_test_error('Perms mismatch: %o perms must be included, but perms %o found' % (attrs['perms'], mode))

    except Exception as exc:
        co.display_err('check_perms failed: %s' % exc)
