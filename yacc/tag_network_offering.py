#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import NetworkOfferings
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

if len(args) == 3:
    Shell(NetworkOfferings()).update(entity=args[1], tags=args[2])

else:
    print('Usage: {} {{offering}} {{tag}}'.format(f))
