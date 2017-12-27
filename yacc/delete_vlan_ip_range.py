#!/usr/bin/python
from resources.resources import VlanIpRanges
from resources.shell import Shell

Shell(VlanIpRanges()).delete_sync()
