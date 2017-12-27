#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import IpAddresses
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

if len(args) == 3:
    Shell(IpAddresses()).associate(ip=args[1], vm=args[2])

elif len(args) == 4:
    Shell(IpAddresses()).associate(ip=args[1], tier=args[2], vm=args[3])

else:
    print('{} {{public-ip}} {{tier}} {{vm}}'.format(f))
    print('  (tier is mandatory in case of associating to vm within vpc)')
