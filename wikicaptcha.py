#! /usr/bin/python
# -*- coding: UTF-8 -*-

# See AUTHORS file for further information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# If not, see <http://www.gnu.org/licenses/>.

# ----- general imports -----
import os
import sys

# ----- module imports -----
from WKCmod import wikidjvu as djv
from WKCmod.parse import parse
from WKCmod.install import WIKICAPTCHA

# ----- global variables definition -----
APPNAME = WIKICAPTCHA['APPNAME']
BASE_DIR = WIKICAPTCHA['BASE_DIR']
CURR_DIR = WIKICAPTCHA['CURR_DIR']

# -----  logging -----
import logging

LOGLEVELS = { logging.CRITICAL: 'CRITICAL',
              logging.ERROR: 'ERROR',
              logging.WARNING: 'WARNING',
              logging.INFO: 'INFO',
              logging.DEBUG: 'DEBUG'}

# --- NullHandler ---
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
# --- END NullHandles

# --- logger formatter ---
LOGFORMAT_STDOUT = { logging.DEBUG: \
         '%(module)s:%(lineno)-4s - %(levelname)-4s: %(message)s',
         logging.INFO: '%(levelname)-8s: %(message)s',
         logging.WARNING: '%(levelname)-8s: %(message)s',
         logging.ERROR: '%(levelname)-8s: %(message)s',
         logging.CRITICAL: '%(levelname)-8s: %(message)s'
       }
# --- END logger formatter ---

# --- root logger ---
rootlogger = logging.getLogger()
rootlogger.setLevel(logging.DEBUG)

lvl_config_logger = logging.DEBUG
#lvl_config_logger = logging.INFO

console = logging.StreamHandler()
console.setLevel(lvl_config_logger)
formatter = logging.Formatter('%(levelname)-8s: %(message)s')
console.setFormatter(formatter)
rootlogger.addHandler(console)

logger = logging.getLogger('wikicaptcha')
# --- END root logger ---

# ----- END logging -----

# ----- option parsing -----
dizcli = parse()

page = dizcli['page']
debug = dizcli['debug']

lvl = logging.WARNING
if debug:
  lvl = logging.DEBUG
  formatter = logging.Formatter(LOGFORMAT_STDOUT[lvl])
  console.setFormatter(formatter)
  console.setLevel(lvl)
else:
  h = NullHandler()
  console.setLevel(lvl)
  rootlogger.addHandler(h)

logger = logging.getLogger(APPNAME)
logger.info("Log level set to: %s" %LOGLEVELS.get(lvl))

djvuinfile_name = dizcli['infile']
djvuinfile = os.path.normpath(os.path.join(CURR_DIR, djvuinfile_name))
logger.info("Input file: %s" %djvuinfile)

# ----- END option parsing ----

# Djvu file object
djvf = djv.wikidjvu(djvuinfile)

# get the list of the words contained in page 2
wl = djvf.get_wordlist_page(2)

# print a list of unclear words (containing a caret ^)
ul = djvf.unclear_caret()
for uw in ul:
  print uw

# produce a TIFF image of the fist unclear word
uw1 = ul[0]
print uw1

tiffoutfile_name = "test/out.tiff"
tiffoutfile = os.path.normpath(os.path.join(CURR_DIR, tiffoutfile_name))

# produce TIFF file, note segment option is WxH+X+Y
command="ddjvu %s -page=%s -format=tiff -segment %sx%s+%s+%s %s" %(djvuinfile, uw1.page, uw1.w, uw1.h, uw1.x, uw1.y, tiffoutfile)
print command
os.system(command)



