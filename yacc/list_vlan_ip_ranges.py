#!/usr/bin/python
# replaced by Nuage version for underlay extensibility
# from resources.resources import VlanIpRanges
from resources.resources import NuageUnderlayVlanIpRanges \
    as VlanIpRanges
from resources.shell import Shell

Shell(VlanIpRanges()).list()
