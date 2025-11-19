#!/usr/bin/env python2
# -*- coding:utf-8 -*-
# getmsgallstr.py

from __future__ import print_function, division, absolute_import

def get_msgall_str(*msgs, **kws):
    if "sep" in kws:
        sep = kws["sep"]
        kws.pop("sep")
    else:
        sep = " "

    positionals_str = ""
    if msgs:
        positionals_str = sep.join(str(m) for m in msgs)

    keywords_str = ""
    if kws:
        keywords_str = sep.join("({k}={v})".format(k=k,v=v) for k, v in kws.items())

    if positionals_str and keywords_str:
        argments_str = sep.join([positionals_str, keywords_str])
    elif positionals_str and not keywords_str:
        argments_str = positionals_str
    elif not positionals_str and keywords_str:
        argments_str = keywords_str
    else:  # if not positionals_str and not keywords_str:
        argments_str = ""

    return argments_str

