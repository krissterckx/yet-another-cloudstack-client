#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import NetworkACLs
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

if len(args) == 4 and args[2].lower() in ['tcp', 'udp', 'icmp']:
    Shell(NetworkACLs()).create(
        acl_list=args[1], protocol=args[2], port=args[3])

elif len(args) == 4:
    Shell(NetworkACLs()).create(
        acl_list=args[1], cidr=args[2], protocol=args[3])

elif len(args) == 5:
    Shell(NetworkACLs()).create(
        acl_list=args[1], cidr=args[2], protocol=args[3], port=args[4])

else:
    print('Usage: '
          '{} {{ACLlist}} [{{cidr}}] {{protocol}} {{port}}'.format(f))
