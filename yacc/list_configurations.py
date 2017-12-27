#!/usr/bin/python
from resources.resources import Configurations
from resources.shell import Shell

Shell(Configurations()).list(
    table_format=True)
