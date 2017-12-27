#!/usr/bin/python
from __future__ import print_function
import sys

from resources.resources import FirewallRules
from resources.shell import Shell

args = sys.argv

if len(args) == 3 and args[1] == 'for-ip':
    Shell(FirewallRules()).print_all(filter_dict={'ip': args[2]})

elif len(args) == 2 and args[1] not in {'-h', '--help'}:
    Shell(FirewallRules()).print_entity(args[1])

elif len(args) == 1:
    Shell(FirewallRules()).print_all()

else:
    print('Usage: {} [{{id or name}}|for-ip {{ip-id}}]'.format(args[0]))
