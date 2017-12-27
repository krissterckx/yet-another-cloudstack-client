#!/usr/bin/python
from resources.resources import FirewallRules
from resources.shell import Shell

Shell(FirewallRules()).delete()
