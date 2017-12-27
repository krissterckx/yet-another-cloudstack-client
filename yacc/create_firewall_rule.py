#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import FirewallRules
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

if len(args) == 4 and args[2].lower() in ['tcp', 'udp', 'icmp']:
    Shell(FirewallRules()).create(
        ip_address=args[1], protocol=args[2], port=args[3],
        short_duration=True
    )

elif len(args) == 4:
    Shell(FirewallRules()).create(
        ip_address=args[1], cidr=args[2], protocol=args[3],
        short_duration=True
    )

elif len(args) == 5:
    Shell(FirewallRules()).create(
        ip_address=args[1], cidr=args[2], protocol=args[3], port=args[4],
        short_duration=True
    )

else:
    print('Usage: '
          '{} {{ip-address}} [{{cidr}}] {{protocol}} {{port}}'.format(f))
