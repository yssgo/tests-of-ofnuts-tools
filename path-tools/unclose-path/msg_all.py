#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from __future__ import print_function, division, absolute_import
from .getmsgallstr import get_msgall_str

def _gimp_msgall_with_handlertype(handlertype, *msgs, **kws):
    from gimpfu import MESSAGE_BOX, pdb
    argments_str = get_msgall_str(*msgs, **kws)

    if handlertype == MESSAGE_BOX:
        if argments_str:
            if argments_str[-1] != "\n":
                argments_str += "\n"
        else:
            argments_str += "\n"

    currenth = pdb.gimp_message_get_handler()
    pdb.gimp_message_set_handler(handlertype)
    pdb.gimp_message(argments_str)
    pdb.gimp_message_set_handler(currenth)
    # end def


def msg_msgbox(*msgs, **kws):
    """msg_msgbox calls Gimp.messgae. the messages are displayed in a Dialog Window.
       If gimp is launched with --console-messages option, the messages are displayed
       to the console.

        msg_msgbox(arg1, arg2, ....., key1=..., key2=..., sep=...)

        The value of keyword argment sep is used as a seperator.
        Other keyword argments are displayed as (key1=...) (key2=...)
    """
    from gimpfu import MESSAGE_BOX
    _gimp_msgall_with_handlertype(MESSAGE_BOX, *msgs, **kws)
    # end def


def msg_console(*msgs, **kws):
    """msg_console calls Gimp.messgae. the messages are displayed in the console.
       If gimp is launched with --console-messages option, the messages are displayed
       to the console.
    #
        msg_console(arg1, arg2, ....., key1=..., key2=..., sep=...)
    #
        The value of keyword argment sep is used as a seperator.
        Other keyword argments are displayed as (key1=...) (key2=...)
    """
    from gimpfu import CONSOLE
    _gimp_msgall_with_handlertype(CONSOLE, *msgs, **kws)
    # end def


def msg_errcon(*msgs, **kws):
    """msg_errcon calls Gimp.messgae. the messages are displayed in the Error Consol Dialog.
       If gimp is launched with --console-messages option, the messages are displayed
       to the console.
    #
        msg_errcon(arg1, arg2, ....., key1=..., key2=..., sep=...)
    #
        The value of keyword argment sep is used as a seperator.
        Other keyword argments are displayed as (key1=...) (key2=...)
    """
    from gimpfu import ERROR_CONSOLE
    _gimp_msgall_with_handlertype(ERROR_CONSOLE, *msgs, **kws)
    # end def
