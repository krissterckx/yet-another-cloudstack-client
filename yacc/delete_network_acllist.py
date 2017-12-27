#!/usr/bin/python
from resources.resources import NetworkACLLists
from resources.shell import Shell

Shell(NetworkACLLists()).delete()
