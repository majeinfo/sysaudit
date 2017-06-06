'''Choose your Python Version'''
import glob
import os
import sys
vers = sys.version_info
if vers.major < 3 and vers.minor < 7:
    print('Python Version must be >= 2.7')
    sys.exit(1)

import plugin
import inspect
from include import compat as co
import sysstore
import socket
import traceback as tb
import argparse

# 1-analysis of command line
parser = argparse.ArgumentParser(description='Audit Tool for Linux System')
parser.add_argument('-s', '--silent', default=False, action='store_true', help='Display Errors only')
parser.add_argument('-p', '--plugin', nargs=1, default=None, action='store', help='Plugin to activate')
cmd_args = parser.parse_args()
co.config(cmd_args)

# Global init
plugins_output = {}
g_plugins_count = 0
g_plugins_run_count = 0
g_tests_count = 0

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
        if inspect.isclass(obj) and issubclass(obj, plugin.Plugin):
            return obj()

    return None

# Loop on Plugins
for fname in sorted(list(glob.glob(full_cur_dir + 'plugins/*.py'))):
    g_plugins_count += 1
    plugin_name = os.path.basename(fname).split('.')[0]

    # Check if plugin must be run
    if cmd_args.plugin and plugin_name not in cmd_args.plugin:
        continue

    plg = load_plugin_file(plugin_name)

    # 3-run audit
    try:
        if plg:
            g_plugins_run_count += 1
            if getattr(plg, 'run', None):
                # unused
                plg.run(plugins_output)
                plugins_output[plugin_name] = plg.output
            else:
                for attr, value in inspect.getmembers(plg):
                    if inspect.ismethod(value) and attr.startswith('check'):
                        #co.begin_test('Execute: ' + attr)
                        g_tests_count += 1
                        plg.begin(attr)
                        (args, varargs, keywords, defaults) = inspect.getargspec(value)
                        if 'plugins_output' in args:
                            value(plugins_output)
                        else:
                            value()
                        plg.end()
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

# Display global Statistics:
print('TOTAL PLUGINS:', g_plugins_count)
print('TOTAL PLUGINS RUN:', g_plugins_run_count)
print('TOTAL TESTS:', g_tests_count)
print('TOTAL WARNINGS:', plugin.Plugin.total_warnings)
print('TOTAL ERRORS:', plugin.Plugin.total_errors)

# EOF