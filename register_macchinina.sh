#!/bin/bash

UUID='[0-9a-f]+-[0-9a-f]+-[0-9a-f]+-[0-9a-f]+-[0-9a-f]+'

# need to find first the ID of "Other Linux (64bit)" using listOsTypes
OTHER_LINUX_64_BIT=`$YACCDIR/api.py listOsTypes | grep -A 4 "Other Linux (64-bit)" | grep "'id'" | grep -oE $UUID`

$YACCDIR/api.py registerTemplate name=macchinina displayText="my own macchinina" url="http://138.203.220.250/images/cloudstack/macchinina/x86_64/macchinina-kvm.qcow2.bz2" zoneids=-1 format=QCOW2 passwordEnabled=true hypervisor=KVM ispublic=true isfeatured=true osTypeId=$OTHER_LINUX_64_BIT
