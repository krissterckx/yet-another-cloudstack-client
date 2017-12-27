#!/usr/bin/python
from resources.resources import NetworkOfferings
from resources.shell import Shell

Shell(NetworkOfferings()).delete_sync()
