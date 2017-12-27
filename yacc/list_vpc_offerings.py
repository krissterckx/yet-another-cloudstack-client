#!/usr/bin/python
from resources.resources import VPCOfferings
from resources.shell import Shell

Shell(VPCOfferings()).list()
