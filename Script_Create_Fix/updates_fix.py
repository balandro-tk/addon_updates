# -*- coding: utf-8 -*-
# ~ --------------------------------------------------------------------------
# ~ *Creates JSON and ZIP files to fix Balandro addon.
# ~     *Find or request for the 'fix' folder.
# ~     *Extracts file list from a 'fix' folder.
# ~     *Generates MD5 from ZIP.
# ~     *Ask for addon version and fix number.
# ~ *ATTENTION: The structure of the fix folder must be the same as the addon.
# ~ --------------------------------------------------------------------------
# ~ *Script Python 3.7 created with PyCharm by Darkozma @ Balandro Team
# ~ --------------------------------------------------------------------------

"""
en-gb = "Instructions: Put the script next to the folder containing the fix files (e.g. updates)."
ca-es = "Instruccions: Posa l'script al costat de la carpeta on hi ha els arxius reparats (p.e. updates)."
es-es = "Instrucciones: Coloca el script junto a la carpeta que contiene los archivos corregidos (p.e. updates)."
"""

script_name = "updates_fix.py"
revision_number = 9
homepage = 'https://www.mimediacenter.info/foro/viewforum.php?f=44'
script_credits = 'All code copyleft (GNU GPL v3) by Darkozma @ Balandro Team'

import os
from os import remove
import shutil
import hashlib
import json


def clean():
    # ~ Delete old version files if they exist.
    if os.path.isfile('updates.json'):
        remove('updates.json')
    if os.path.isfile('updates.zip'):
        remove('updates.zip')


def pth_fixdir():
    # ~ Set current path and fix folder.
    pth = os.getcwd()

    if os.path.isdir('updates'):
        fixdir = 'updates'
    else:
        fixdir = input("\nSorry, 'updates' folder not found. Type your fixes folder name: \n")
        fix_isdir = os.path.isdir(fixdir)
        while not fix_isdir:
            fixdir = input("Sorry, '%s' folder not found. Type your fixes folder name: \n" % fixdir)
            fix_isdir = os.path.isdir(fixdir)

    return pth, fixdir


def versions():
    # ~ Set addon and fix versions.
    addon_version = input("Type addon version: \n")
    fix_version = input("Type fix number: \n")

    return addon_version, fix_version


def prep_fix():
    # ~ Prepare fix if 0 version -dummy- or not.
    if os.path.isfile(os.path.join(fixdir, 'fix0')):
        remove(os.path.join(fixdir, 'fix0'))
    if fix_version == '0':
        with open(os.path.join(fixdir, 'fix0'), 'a') as fix0:
            fix0.write('fix0')


def create_zip():
    # ~ Create zip file and generate MD5.
    prep_fix()
    shutil.make_archive("updates", "zip", root_dir=os.path.join(pth, fixdir))

    with open('updates.zip', 'rb') as fz:
        md5 = hashlib.md5()

        for chunk in iter(lambda: fz.read(4096), b""):
            md5.update(chunk)
        hash_updates_zip = md5.hexdigest()

    return hash_updates_zip


def create_json():
    # ~ Create JSON for Fix > 0
    fixdict = {'hash': hash_updates_zip, 'addon_version': addon_version, 'fix_version': int(fix_version)}
    filesdict = {}

    rootdir = os.listdir(os.path.join(pth, fixdir))
    elselist = []

    for dirs in rootdir:
        iflist = []

        if os.path.isdir(os.path.join(pth, fixdir, dirs)):
            dirlist = os.listdir(os.path.join(pth, fixdir, dirs))
            for fil in dirlist:
                basename, ext = os.path.splitext(fil)
                if basename not in iflist:
                    iflist.append(basename)
            iflist.sort()
            filesdict[dirs] = iflist
        elif os.path.isfile(os.path.join(pth, fixdir, dirs)):
            basename, ext = os.path.splitext(dirs)
            elselist.append(basename)
            elselist.sort()
            filesdict['root dir'] = elselist

    fixdict['files'] = filesdict

    with open('updates.json', 'a') as fix:
        fix.write(json.dumps(fixdict, indent=4, sort_keys=True, skipkeys=True, ensure_ascii=False))


def create_f0info():
    # ~ Create JSON for fix0 and/or ending info.
    zipped = 'ZIP'
    if fix_version == '0':
        zipped = 'Dummy ZIP'
        fixdict = {'hash': hash_updates_zip, 'addon_version': addon_version}
        with open('updates.json', 'a') as fix:
            fix.write(json.dumps(fixdict, indent=4, sort_keys=True, skipkeys=True, ensure_ascii=False))
    print('\nFix %s for Balandro %s created (JSON + %s).\n%s MD5: %s\n    *%s --> version %s'
          '\n        More info: %s\n            %s' % (fix_version, addon_version, zipped, zipped, hash_updates_zip,
                                                       script_name, revision_number, homepage, script_credits))


def global_var():
    # ~ Launch the initial functions.
    pth, fixdir = pth_fixdir()
    addon_version, fix_version = versions()
    clean()

    return pth, fixdir, addon_version, fix_version


def ending():
    # ~ Launch last functions.
    if fix_version != '0':
        create_json()
    create_f0info()


pth, fixdir, addon_version, fix_version = global_var()
hash_updates_zip = create_zip()
ending()
