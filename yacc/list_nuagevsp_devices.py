#!/usr/bin/python
from resources.resources import NuageVspDevices
from resources.shell import Shell
import sys

args = sys.argv

if len(args) == 2:
    Shell(NuageVspDevices()).list_by_parent(args[1])

else:
    print('Usage: {} {{physical-network}}'.format(args[0]))
