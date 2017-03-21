'''Compatibility Module for different Python Versions'''
from __future__ import absolute_import, division, print_function, unicode_literals
import sys

# TODO: ajouter de la couleur...

debug_flag = False
silent = False
py_major, py_minor = sys.version_info[:2]

bold = "\033[1m{0}\033[0m"
color_red = "\033[1;31m{0}\033[00m"
color_cya = "\033[1;36m{0}\033[00m"
color_grn = "\033[1;32m{0}\033[00m"


def config(args):
    global silent
    silent = args.silent


def display(*args):
    print(*args)


def display_plugin(plugin_name):
    if not silent: display(color_cya.format('PLUGIN>'), bold.format(plugin_name))


def display_err(*args):
    print(color_red.format('ERROR:'), *args, file=sys.stdout)


def begin_test(*args):
    if not silent: print(*args, end='')


def end_test_ok(*args):
    print(':', color_grn.format('OK'), *args)


def end_test_failed(*args):
    print(':', color_red.format('FAILED'), *args)


def display_ok(msg, indent=False):
    if not silent: print('\t' if indent else '', color_grn.format('OK'), msg)


def display_info(msg, indent=False):
    if not silent: print('\t' if indent else '', color_grn.format('INFO'), msg)


def display_warning(msg, indent=False):
    if not silent: print('\t' if indent else '', color_grn.format('WARN'), msg)


def display_err(msg, indent=False):
    print('\t' if indent else '', color_red.format('ERROR:'), msg, file=sys.stdout)


def test_error(*args):
    display_err(*args)


def debug(*args):
    if debug_flag: display('DEBUG:', *args)