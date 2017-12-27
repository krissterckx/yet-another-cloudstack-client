#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import SSHKeyPairs 
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

if len(args) == 3:
    Shell(SSHKeyPairs()).register(
        name=args[1], public_key=args[2])

else:
    print('Usage: {{name}} {{publickey}}'.format(f))
