#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.resources import VirtualMachines
from resources.shell import Shell


def to_array(networks):
    return [net for net in networks.split(',')]


args = sys.argv
f = os.path.basename(args[0])
until_c = Shell.define_until_completion(args, False)
vm = None

if len(args) == 3:
    vm = Shell(VirtualMachines()).deploy(
        name=args[1], networks=to_array(args[2]),
        until_completion=until_c, short_duration=False)

elif len(args) == 4:
    vm = Shell(VirtualMachines()).deploy(
        name=args[1], networks=to_array(args[2]), template=args[3],
        until_completion=until_c, short_duration=False)

elif len(args) == 5:
    vm = Shell(VirtualMachines()).deploy(
        name=args[1], networks=to_array(args[2]), template=args[3],
        keypair=args[4], until_completion=until_c,
        short_duration=False)

else:
    print('Usage: {} [--(a)sync] {{name}} {{network}}[,{{network}}] '
          '[{{template}}] [{{keypair}}]'.format(f))

if vm and until_c and isinstance(vm, dict) and 'nic' in vm:
    if len(vm['nic']) == 1:
        print('Its ip address is %s' % vm['nic'][0]['ipaddress'])
    elif len(vm['nic']) > 1:
        ips = ','.join(nic['ipaddress'] for nic in vm['nic'])
        print('IPAddress: %s' % ips)
