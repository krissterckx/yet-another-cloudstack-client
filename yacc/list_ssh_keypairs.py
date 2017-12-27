#!/usr/bin/python
from resources.resources import SSHKeyPairs
from resources.shell import Shell

Shell(SSHKeyPairs()).list()
