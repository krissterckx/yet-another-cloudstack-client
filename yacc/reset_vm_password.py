#!/usr/bin/python
from resources.resources import VirtualMachines
from resources.shell import Shell

Shell(VirtualMachines()).reset(
    VirtualMachines.PASSWORD_FOR_VM, VirtualMachines.PASSWORD)
