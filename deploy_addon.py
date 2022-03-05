#!/usr/bin/env python
# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: romanvm@yandex.ua
# License: GPL v.3 <http://www.gnu.org/licenses/gpl-3.0.en.html>
"""
Deploy Kodi addons to my repository and/or publish Sphinx docs to GitHub Pages
"""

from __future__ import print_function
import re
import os
import shutil
import argparse
from subprocess import call

gh_token = os.environ['GH_TOKEN']
devnull = open(os.devnull, 'w')


# Utility functions
def execute(args, silent=False):
    if silent:
        stdout = stderr = devnull
    else:
        stdout = stderr = None
    call_string = ' '.join(args).replace(gh_token, '*****')
    print('Executing: ' + call_string)
    res = call(args, stdout=stdout, stderr=stderr)
    if res:
        raise RuntimeError('Call {call} returned error code {res}'.format(
            call=call_string,
            res=res
        ))


def clean_pyc(folder):
    cwd = os.getcwd()
    os.chdir(folder)
    paths = os.listdir(folder)
    for path in paths:
        abs_path = os.path.abspath(path)
        if os.path.isdir(abs_path):
            clean_pyc(abs_path)
        elif path[-4:] == '.pyc':
            os.remove(abs_path)
    os.chdir(cwd)


def create_zip(zip_name, root_dir, addon):
    clean_pyc(os.path.join(root_dir, addon))
    shutil.make_archive(zip_name, 'zip', root_dir=root_dir, base_dir=addon)
    print('ZIP created successfully.')


# Argument parsing
parser = argparse.ArgumentParser(description='Deploy an addon to my Kodi repo and/or publish docs on GitHub Pages')
parser.add_argument('-z', '--zip', help='pack addon into a ZIP file', action='store_true')
parser.add_argument('addon', nargs='?', help='addon ID', action='store', default='')
parser.add_argument('-v', '--version', nargs='?', help='read addon version from xml and write it to a specified file', default='version')
args = parser.parse_args()
# Define paths
if not args.addon:
    addon = os.environ['ADDON']
else:
    addon = args.addon
root_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(root_dir, addon, 'addon.xml'), 'rb') as addon_xml:
    version = re.search(r'(?<!xml )version="(.+?)"', addon_xml.read()).group(1)
zip_name = '{0}-{1}'.format(addon, version)
zip_path = os.path.join(root_dir, zip_name + '.zip')
# Start working
os.chdir(root_dir)
if args.zip:
    create_zip(zip_name, root_dir, addon)
if args.version:
    _path = os.path.join(root_dir, args.version)
    # print(_path)
    with open(_path, "w") as file:
        file.write(version)