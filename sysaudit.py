'''Choose your Python Version'''
import glob
import os
import sys
vers = sys.version_info
if vers.major < 3 and vers.minor < 7:
    print 'Python Version must be >= 2.7'
    sys.exit(1)

import inspect
from include import compat as co
import sysstore
import socket
import traceback as tb
import argparse

# 1-analysis of command line
parser = argparse.ArgumentParser(description='Audit Tool for Linux System')
parser.add_argument('-s', '--silent', default=False, action='store_true', help='Display Errors only')
args = parser.parse_args()
co.config(args)

# Global init
plugins_output = {}

if sys.argv[0][0] == '/':
    full_cur_dir = os.path.dirname(sys.argv[0]) + os.sep
else:
    full_cur_dir = os.path.dirname('./' + sys.argv[0]) + os.sep

sys.path = [full_cur_dir + 'plugins/' ] + sys.path

# 2-scan plugins directory
def load_plugin_file(plugin_name):
    co.display_plugin(plugin_name)
    try:
        mod = __import__(os.path.basename(plugin_name))
    except Exception as exc:
        co.display_err('Could not import %s module' % plugin_name)
        co.display_err(exc)
        tb.print_exc()
        return None

    for member, obj in inspect.getmembers(mod):
        if inspect.isclass(obj):
            return obj()    # TODO: devrait tester que derive de Plugin

    return None


for fname in sorted(list(glob.glob(full_cur_dir + 'plugins/*.py'))):
    plugin_name = os.path.basename(fname).split('.')[0]
    plg = load_plugin_file(plugin_name)
    # 3-run audit
    try:
        if plg:
            if getattr(plg, 'run', None):
                plg.run(plugins_output)
                plugins_output[plugin_name] = plg.output
            else:
                for attr, value in inspect.getmembers(plg):
                    if inspect.ismethod(value) and attr.startswith('check'):
                        value(plugins_output)
                plugins_output[plugin_name] = plg.output

    except Exception as exc:
        co.display_err('Execution of plugin %s failed' % plugin_name)
        co.display_err(exc)
        tb.print_exc()

# Store audit result in JSON file
# TODO: change le nom
conf = sysstore.SysStore('conf.json')
my_hostname = socket.gethostname().split('.')[0]
print(plugins_output)

# EOF