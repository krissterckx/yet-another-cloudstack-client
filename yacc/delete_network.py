#!/usr/bin/python
from resources.resources import Networks
from resources.shell import Shell

Shell(Networks()).delete()
