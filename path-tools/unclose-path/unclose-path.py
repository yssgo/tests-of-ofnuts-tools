#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GIMP plugin to reopen closed strokes
# (c) Ofnuts 2011
#
#   History:
#
#   v0.0: 2011-04-09 first published version
#   v0.1: 2011-04-25 move to <Vectors>/Tools
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

#
#   MODIFICATION History:
#
#   2025-11-19: Senu Iun : Modified to be translatable
#   2024-07-26: MENU ITEMS GROUPED UNDER .../Ofnuts/... BY SSIUN
#   2024-07-26: BUGS FIXED: SSIUN REPLACED 'print' WITH 'pass #print' AS IT CAUSES ERRORS ON WINDOWS
#

from __future__ import print_function, division
import os, sys, gettext, webbrowser
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pathlib_py27 import Path as Filepath
from msg_all_py27 import get_msgall_str, msg_errcon, msg_msgbox
filebase = Filepath(__file__).stem
locale_dir = str(Filepath(__file__).absolute().parent/'locale')
gettext.install(filebase, locale_dir, unicode=True)
GETTEXT_TRANSLATE = _
_ = GETTEXT_TRANSLATE

N_ = lambda msg: msg

PYCON_MODE = os.path.basename(sys.argv[0]) == 'python-console.py'
DEBUG_MODE = False
DEBUG_MODE = os.environ.get('DEBUG_MODE', str(DEBUG_MODE)).lower() in ['1', 'on', 'yes', 'true']
from gimpfu import *

def print_trace(*a, **k):
    if PYCON_MODE:
        print(get_msgall_str(*a, **k))
    else:
        msg_errcon(*a, **k)


def trace(*a, **k):
    if DEBUG_MODE:
        print_trace(*a, **k)

debug_trace = lambda *a, **k: trace(*a, **k)

def dumpStroke(stroke):
    print_trace('------------------------')
    print_trace('>>> %s +++' % stroke)
    
    length=stroke.get_length(0.1)
    (points,closed)=stroke.points
    print_trace('>>> Length: %7.2f, closed: %s' % (length,closed))
    print_trace('>>> Points: %s' % (len(points)//6,) )
    for i in range(0,len(points),6):
        xc1=points[i+0]
        yc1=points[i+1]
        xp0=points[i+2]
        yp0=points[i+3]
        xc2=points[i+4]
        yc2=points[i+5]
        print_trace('***\t%7.2f\t%7.2f\t%7.2f\t%7.2f\t%7.2f\t%7.2f' % (xc1,yc1,xp0,yp0,xc2,yc2))
    print_trace('----------')


# Attempst to detect if the stroke is really closed. 
# Open strokes have no handles at their extremities, 
# so the handle coordinates are identical to 
# those of the termination point.
# Conversely, if the handle coordinates are not 
# those of the termination point the stroke
# can be considered closed.
def looksClosed(points):
    
    # Test for no handles
    closed1=(points[+0]!=points[+2]) or (points[+1]!=points[+3])
    closed2=(points[-1]!=points[-3]) or (points[-2]!=points[-4])
    # Test for identical extremities
    closed3=(points[+2]==points[-4]) or (points[+3]==points[-4])
    
    if closed1:
        print_trace('Handle at %7.2f,%7.2f' % (points[+2],points[+3]))
    if closed2:
        print_trace('Handle at %7.2f,%7.2f' % (points[-3],points[-4]))
    if closed3:
        print_trace('Closed at %7.2f,%7.2f' % (points[+2],points[+3]))
    return closed1 or closed2 or closed3

def unclose(image,closedPath):
    try:
        openPath=pdb.gimp_vectors_new(image, 'Unclosed '+closedPath.name)
        pdb.gimp_image_add_vectors(image, openPath, 0)

        for closedStroke in closedPath.strokes:
            print_trace('Copying stroke: %s' % closedStroke)
            points,closed=closedStroke.points
            #if not looksClosed(points):
                #closed=0
            closed = 0
            sid = pdb.gimp_vectors_stroke_new_from_points(openPath,0, len(points),points, closed)
        openPath.visible=True
    except Exception as e:
        print_trace(e.args[0])
        pdb.gimp_message(e.args[0])

    pdb.gimp_displays_flush()
    return;


### Registration
whoiam='\n'+os.path.abspath(__file__)

register(
    "unclose-path",
    _("Re-open path strokes...")+whoiam,
    _("Re-open path strokes..."),
    "Ofnuts",
    "Ofnuts",
    "2011",
    _("Unclose"),
    "*",
    [
        (PF_IMAGE, "image", _("Input image"), None),
        (PF_VECTORS, "refpath", _("Input path"), None),
    ],
    [],
    unclose,
    # FOR TRANSLATORS: Don't translate '<Vectors>/'
    menu="<Vectors>/Ofnuts/Tools",
    domain=(filebase, locale_dir)
)

def open_the_help_document(image=None, item=None):
    '''opens the help document( Doc/unclose-path-{lang}.html or
    unclose-path.html).

    the parameters(image and item) are not used at all.
    however they are required for the `register` function.
    '''
    debug_trace('open_the_help_document started!')
    file_stem = 'unclose-path'
    default_help_fpath = Filepath(
        __file__).parent / 'Doc' / '{file_stem}.html'.format(**locals())
    mo_file = gettext.find(filebase, localedir=locale_dir)
    if mo_file and 'locale' in mo_file:
        lang_pos = mo_file.find('locale') + 7
        lang_stop = mo_file.find('LC_MESSAGES') - 1
        lang_found = mo_file[lang_pos:lang_stop]
    else:
        lang_found = None
    if lang_found is not None:
        help_fpath = Filepath(
            __file__).parent / 'Doc' / '{file_stem}-{lang}.html'.format(
                lang=lang_found, **locals())
    else:
        help_fpath = default_help_fpath
    if not help_fpath.is_file():
        help_fpath = default_help_fpath
    fullpathname = str(help_fpath.absolute())
    if help_fpath.is_file():
        webbrowser.open('file://' + fullpathname)
        return True
    else:
        msg_errcon(
            "Help document({fullpathname}) not found.".format(**locals()))
        raise Exception(_("Help document not found."))
        return False

register(
    "unclose-path-help-document",
     _("Open the HTML help file for for ‘Unclose’.\n"
      "The name of the file is 'unclose-path[-LANG].html'."),
    _("Open the help document for ‘Unclose’"),
    'Sensu Iun',
    'GNU General Public License 3.0 or later',
    '2025',
    _('Help for ‘Unclose’'),
    "*",
    [
        (PF_IMAGE, "image", _("Input image"), None),
        (PF_VECTORS, "refpath", _("Input path"), None),
    ],
    [],
    open_the_help_document,
    # FOR TRANSLATORS: Don't translate '<Vectors>/'
    menu="<Vectors>/Ofnuts/Tools",
    domain=(filebase, locale_dir)
)
if not PYCON_MODE:
    main()
