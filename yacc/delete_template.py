#!/usr/bin/python
from resources.resources import Templates
from resources.shell import Shell

Shell(Templates()).delete()
