#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import VPCs
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

if len(args) == 4 and args[1] != '--sync':
    Shell(VPCs()).create_async(name=args[1], offering=args[2], cidr=args[3])

elif len(args) == 5 and args[1] == '--sync':
    Shell(VPCs()).create_async(name=args[2], offering=args[3], cidr=args[4],
                               until_completion=True)

else:
    print('Usage: {} [--sync] {{name}} {{vpc-offering}} {{cidr}}'.format(f))
