""" Stub Generator for Spotfire dlls using IronPython

Extended script based on script developed by Gary Edwards at:
gitlab.com/reje/revit-python-stubs
and Gui Talarico at https://github.com/gtalarico/ironpython-stubs

This is uses a slightly modify version of generator3,
github.com/JetBrains/intellij-community/blob/master/python/helpers/generator3.py

Iterates through a list of targeted assemblies and generates stub directories
for the namespaces using pycharm's generator3.

MIT LICENSE
https://github.com/gtalarico/ironpython-stubs
Pete Thompson
"""

import sys
import os
import json
import re

from utils.docopt import docopt
from utils.logger import logger
from utils.helper import Timer
from make_stubs import make, dump_json_log

__version__ = '1.0.0'
__doc__ = """
    Spotfire-python-stubs | {version}

    Spotfire Python Stubs Generator

    Usage:
      stubs --spotfire=<dir> [--overwrite --debug --no-json]
      stubs --help

    Examples:
      ipy -m stubs --spotfire="c:\spotfire\modules"
      ipy -m stubs --help

    Options:
        --spotfire=<dir>        Name of the Spotfire modules folder
        --overwrite             Force Overwrite if stub already exists [default: False].
        --no-json               Disables Json Log
        --debug                 Enables Debug Messages
        -h, --help              Show this screen.

    """.format(version=__version__)

arguments = docopt(__doc__, version=__version__)

# OPTIONS
option_spotfire_modules_folder = arguments['--spotfire']
option_overwrite = arguments['--overwrite']
option_json = not arguments['--no-json']

if arguments['--debug']:
    logger.enable_debug()

logger.debug(arguments)

# Determine the output directory
PKG_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(PKG_DIR)
release_dir = os.path.join(PROJECT_DIR, 'spotfire-stubs')
os.chdir(PROJECT_DIR)

# Scan the modules folder for subfolders and add those to the system path variable and pick out the dlls to load
logger.debug('checking Spotfire modules at: ' + option_spotfire_modules_folder)
ASSEMBLIES = []
for root, dirs, files in os.walk(option_spotfire_modules_folder):
    [sys.path.append(os.path.join(option_spotfire_modules_folder, p)) for p in dirs]
    ASSEMBLIES.extend([re.sub(r'.dll$', '', dll) for dll in files if (dll.lower().endswith('.dll'))])

ASSEMBLIES.sort()

logger.debug('Paths: ' + str(sys.path))
logger.debug('Assemblies: ' + str(ASSEMBLIES))

timer = Timer()

for assembly_name in ASSEMBLIES:
    assembly_dict = make(release_dir, assembly_name,
                         overwrite=option_overwrite, quiet=True)
    if option_json:
        dump_json_log(assembly_dict)
logger.info('Done: {} seconds'.format(timer.stop()))
