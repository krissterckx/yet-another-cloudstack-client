#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import PhysicalNetworks 
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

if len(args) == 2:
    Shell(PhysicalNetworks()).create(
        name=args[1], zone=args[2], isolation_method=args[3])

else:
    print('Usage: {} {{name}} [{zone}} {{isolation-method}}]'.format(f))
