#!/usr/bin/python
import sys

from resources.resources import Hosts
from resources.shell import Shell

args = sys.argv

if len(args) == 1:
    Shell(Hosts()).print_all()

elif len(args) == 2 and args[1] not in {'-h', '--help'}:
    if args[1] == 'capacity':
        Shell(Hosts()).print_capacity()
    else:
        Shell(Hosts()).print_entity(args[1])

elif len(args) > 2:
    args.pop(0)
    Shell(Hosts()).print_entities(args)

else:
    print('Usage: {} [capacity|[table] {{host}}*]'.format(args[0]))
