#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import IpAddresses
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

until_c = Shell.define_until_completion(args, True)

if len(args) == 2 and args[1] not in {'network', 'vpc'}:
    Shell(IpAddresses()).acquire(
        network_or_vpc=args[1], until_completion=until_c)

elif len(args) == 3 and args[1] not in {'network', 'vpc'}:
    Shell(IpAddresses()).acquire(
        network_or_vpc=args[1], vm=args[2], until_completion=until_c)

elif len(args) == 3 and args[1] in {'network', 'vpc'}:
    if args[1] == 'network':
        Shell(IpAddresses()).acquire(
            network=args[2], until_completion=until_c)
    else:
        Shell(IpAddresses()).acquire(
            vpc=args[2], until_completion=until_c)

elif len(args) == 4 and args[1] in {'network', 'vpc'}:
    if args[1] == 'network':
        Shell(IpAddresses()).acquire(
            network=args[2], vm=args[2], until_completion=until_c)
    else:
        Shell(IpAddresses()).acquire(
            vpc=args[2], vm=args[2], until_completion=until_c)

else:
    print('{} [--(a)sync] [network|vpc] {{network|vpc}} [{{vm}}]'.format(f))
