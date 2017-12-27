#!/usr/bin/python
from __future__ import print_function
import os
import sys

args = sys.argv
ext = '.py'

if len(args) > 2:
    if (args[1] == 'show' and args[2] == 'capacity' or
        args[1] == 'deploy' and args[2] == 'application' or
        args[1] == 'list' and args[2] == 'capacity_settings'):
        ext = '.sh'
    elif args[1] == 'show':
        args[1] = 'list'
        args.insert(3, '--deep')
    if args[1] == 'destroy' and args[2] != 'virtual_machine':
        args[1] = 'delete'
        args.insert(3, '--deep')
    f = os.environ['YACCDIR'] + '/' + args[1] + '_' + args[2]
    if args[1] == 'list' and args[2][-1:] != 's':
        f += 's'
    f += ext
    del args[:3]

    # i know it is retarded, but quick way to get job done
    if os.path.isfile(f):
        os.system(f + ' ' + ' '.join(a for a in args))
    else:
        print('Sorry, I don\'t know what you mean (%s).' % f)

else:
    print('Usage: yacc {{verb}} {{resource}} [{{args}}]')
