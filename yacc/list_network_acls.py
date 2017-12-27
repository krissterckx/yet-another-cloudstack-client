#!/usr/bin/python
from resources.resources import NetworkACLs
from resources.shell import Shell

Shell(NetworkACLs()).list()
