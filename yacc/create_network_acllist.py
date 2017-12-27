#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import NetworkACLLists
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

if len(args) == 3:
    Shell(NetworkACLLists()).create(
        name=args[1], vpc=args[2])

elif len(args) == 4:
    Shell(NetworkACLLists()).create(
        name=args[1], description=args[2], vpc=args[3])

else:
    print('Usage: {} {{name}} [{{description}}] {{vpc}}'.format(f))
