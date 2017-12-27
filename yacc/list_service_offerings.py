#!/usr/bin/python
from resources.resources import ServiceOfferings
from resources.shell import Shell

Shell(ServiceOfferings()).list()
