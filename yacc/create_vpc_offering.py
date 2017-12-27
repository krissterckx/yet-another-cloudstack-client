#!/usr/bin/python
from __future__ import print_function
import sys

from resources.resources import VPCOfferings
from resources.shell import Shell

args = sys.argv

if len(args) == 2 and args[1] in {'nuage', 'nuage_configdrive'}:
    Shell(VPCOfferings()).create_async(
        short_duration=True, keyword=args[1], until_completion=True)

elif (len(args) == 3 and args[1] in {'nuage', 'nuage_configdrive'} and
      args[2] != 'no-userdata'):
    Shell(VPCOfferings()).create_async(
        short_duration=True, keyword=args[1], name=args[2],
        until_completion=True)

elif (len(args) == 3 and args[1] in {'nuage', 'nuage_configdrive'} and
      args[2] == 'no-userdata'):
    Shell(VPCOfferings()).create_async(
        short_duration=True, keyword=args[1], user_data=False,
        until_completion=True)

elif (len(args) == 3 and args[1] in {'nuage', 'nuage_configdrive'} and
      args[3] == 'no-userdata'):
    Shell(VPCOfferings()).create_async(
        short_duration=True, keyword=args[1], name=args[2], user_data=False,
        until_completion=True)

else:
    print('Usage: {} nuage|nuage_configdrive [{{name}}] '
          '[no-userdata]'.format(args[0]))
