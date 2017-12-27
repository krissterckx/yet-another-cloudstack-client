#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import IpAddresses
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

if len(args) == 2:
    Shell(IpAddresses()).disassociate(ip=args[1], until_completion=False)

else:
    print('{} {{public-ip}}'.format(f))
