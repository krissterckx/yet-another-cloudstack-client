#!/usr/bin/python
from __future__ import print_function

from yacc.resources.resources import NetworkOfferings
from yacc.resources.resources import Networks
from yacc.resources.resources import VirtualMachines
from yacc.resources.settings import Settings


def deploy_destroy_server():
    Settings().set_until_completion()

    net_off = NetworkOfferings().create('nuage_isolated', skip_if_exists=True)

    net = Networks().create('test', offering=net_off, cidr='10.10.1.1/24')
    print('Deployed a network.')

    instance = VirtualMachines().deploy('test', [net])
    print('Deployed a machine.')

    VirtualMachines().delete(instance)
    print('Destroyed machine.')

    Networks().delete(net)
    print('Deleted network.')
