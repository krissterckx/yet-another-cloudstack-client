#!/usr/bin/python
from resources.resources import NuageVspDevices
from resources.shell import Shell
import sys

args = sys.argv

if len(args) == 4:
    Shell(NuageVspDevices()).update(phys_net=args[1],
                                    username=args[2],
                                    password=args[3])

else:
    print('Usage: {} {{physical-network}} {{username}} {{password}}'.
          format(args[0]))
