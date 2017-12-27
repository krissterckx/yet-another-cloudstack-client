#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import Networks
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

# mind that networks are created synchronously all the time !
if len(args) > 1 and args[1] == 'sync':
    print('Networks are created synchronously, can\'t specify sync.')

elif len(args) == 4 and Shell.check_cidr(args[3]):
    s = Shell(Networks()).create(name=args[1], offering=args[2], cidr=args[3])
    if 'shared' in args[2].lower():
        s.on_success('Mind that an IPRange must be added before a '
                     'shared network is usable.')

elif len(args) == 5 and Shell.check_cidr(args[3]):
    Shell(Networks()).create(name=args[1], offering=args[2], cidr=args[3],
                             vpc=args[4])

elif len(args) == 6 and Shell.check_cidr(args[3]) and args[4] == 'ext':
    Shell(Networks()).create(name=args[1], offering=args[2], cidr=args[3],
                             externalid=args[5])

elif len(args) == 7 and Shell.check_cidr(args[3]) and args[5] == 'ext':
    Shell(Networks()).create(name=args[1], offering=args[2], cidr=args[3],
                             vpc=args[4], externalid=args[6])

elif len(args) == 6 and Shell.check_cidr(args[3]) and args[4] == 'vlan':
    Shell(Networks()).create(name=args[1], offering=args[2], cidr=args[3],
                             vlan=args[5])

elif len(args) == 7 and Shell.check_cidr(args[3]) and args[5] == 'vlan':
    Shell(Networks()).create(name=args[1], offering=args[2], cidr=args[3],
                             vpc=args[4], vlan=args[6])

elif len(args) == 6 and Shell.check_cidr(args[3]):
    Shell(Networks()).create(name=args[1], offering=args[2], cidr=args[3],
                             vpc=args[4], acl=args[5])

else:
    print('Usage: {} {{name}} {{network-offering}} {{cidr}} [{{vpc}}] '
          '[{{acl}}] [ext {{externalid}}] [vlan {{vlan}}]'.format(f))
