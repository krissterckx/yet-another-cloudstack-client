#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import VPCOfferings
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

if len(args) == 3:
    Shell(VPCOfferings()).update(entity=args[1], tags=args[2],
                                 asynchronous=True)

else:
    print('Usage: {} {{offering}} {{tag}}'.format(f))
