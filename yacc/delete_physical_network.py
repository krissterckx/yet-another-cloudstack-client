#!/usr/bin/python
from resources.resources import PhysicalNetworks
from resources.shell import Shell

Shell(PhysicalNetworks()).delete()
