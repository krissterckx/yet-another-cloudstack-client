#!/usr/bin/python
from resources.resources import VPCs
from resources.shell import Shell

Shell(VPCs()).restart()
