#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import Networks
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])
until_c = Shell.define_until_completion(args, True)

if len(args) == 3:
    Shell(Networks()).migrate(network=args[1], offering=args[2],
                              until_completion=until_c)

elif len(args) == 4 and args[3] == 'resume':
    Shell(Networks()).migrate(network=args[1], offering=args[2],
                              resume=True, until_completion=until_c)

else:
    print('Usage: {} [--(a)sync] {{network}} {{offering}} [resume]'.format(f))
