#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import VPCs 
from resources.shell import Shell

args = sys.argv
f = os.path.basename(args[0])
until_c = Shell.define_until_completion(args, True)


def parse_net_offerings(net_offerings):
    net_offerings = [net_off for net_off in net_offerings.split(',')]
    net_to_off = {}
    for net_off in net_offerings:
        n_o = net_off.split('=')
        net_to_off[n_o[0]] = n_o[1]
    return net_to_off 


if len(args) == 4:
    Shell(VPCs()).migrate(vpc=args[1], offering=args[2],
                          network_offerings=parse_net_offerings(args[3]),
                          until_completion=until_c)

elif len(args) == 5 and args[4] == 'resume':
    Shell(VPCs()).migrate(vpc=args[1], offering=args[2],
                          network_offerings=parse_net_offerings(args[3]),
                          resume=True, until_completion=until_c)

else:
    print('Usage: {} [--(a)sync] {{vpc}} {{offering}} {{network=offering,...}} [resume]'.format(f))
