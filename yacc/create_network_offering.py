#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import NetworkOfferings
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])

if len(args) > 1 and args[1] in {'shared',
                                 'shared_configdrive',
                                 'isolated',
                                 'isolated_configdrive',
                                 'nuage_shared',
                                 'nuage_shared_configdrive',
                                 'nuage_isolated',
                                 'nuage_isolated_configdrive'}:

    if len(args) == 2:
        Shell(NetworkOfferings()).create(
            keyword=args[1], short_duration=True).exit()

    elif len(args) == 3 and args[2] == 'for-vpc':
        Shell(NetworkOfferings()).create(
            keyword=args[1], short_duration=True, for_vpc=True).exit()

    elif len(args) == 3 and args[2] != 'for-vpc' and args[2] != 'no-userdata':
        Shell(NetworkOfferings()).create(
            keyword=args[1], short_duration=True, name=args[2]).exit()

    elif len(args) == 4 and args[2] == 'for-vpc' and args[3] != 'no-userdata':
        Shell(NetworkOfferings()).create(
            keyword=args[1], short_duration=True, name=args[3],
            for_vpc=True).exit()

    elif len(args) == 3 and args[2] != 'for-vpc' and args[2] == 'no-userdata':
        Shell(NetworkOfferings()).create(
            keyword=args[1], short_duration=True, user_data=False).exit()

    elif len(args) == 4 and args[2] == 'for-vpc' and args[3] == 'no-userdata':
        Shell(NetworkOfferings()).create(
            keyword=args[1], short_duration=True, user_data=False,
            for_vpc=True).exit()

print('Usage: {} (nuage_)shared|(nuage_)shared_configdrive|(nuage_)isolated|'
      '(nuage_)isolated_configdrive '
      '[for-vpc] [{{name}}] [no-userdata]'.format(f))
