#!/usr/bin/python
import sys

from resources.resources import Resources

args = sys.argv

if len(args) == 2:
    Resources(exit_on_bad_request=True).snd_rcv(args[1], output=True)

elif len(args) > 2:
    args_d = {}
    for arg in range(2, len(args)):
        key_value = str(args[arg]).split('=')
        args_d[key_value[0]] = key_value[1]
    Resources(exit_on_bad_request=True).snd_rcv(args[1], args_d, output=True)

else:
    print('Usage: {} {{request}} {{parameter=value}}*'.format(args[0]))
