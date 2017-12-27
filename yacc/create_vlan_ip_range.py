#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import VlanIpRanges
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

if len(args) == 2:
    Shell(VlanIpRanges()).create(cidr=args[1])

elif len(args) == 3:
    Shell(VlanIpRanges()).create(cidr=args[1], network=args[2])

elif len(args) == 4 and args[2] == 'vlan':
    Shell(VlanIpRanges()).create(cidr=args[1], vlan=args[3])

elif len(args) == 4:
    Shell(VlanIpRanges()).create(
        cidr=args[1], start_ip=args[2], end_ip=args[3])

elif len(args) == 5:
    Shell(VlanIpRanges()).create(
        cidr=args[1], start_ip=args[2], end_ip=args[3], network=args[4])

elif len(args) == 6 and args[4] == 'vlan':
    Shell(VlanIpRanges()).create(
        cidr=args[1], start_ip=args[2], end_ip=args[3], vlan=args[5])

else:
    print('Usage: '
          '{} {{cidr}} [{{start-ip}} {{end-ip}}] [{{network}}] [vlan {{vlan}}]'.format(f))
