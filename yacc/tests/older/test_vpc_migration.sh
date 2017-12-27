#!/bin/bash

COMMAND=`echo $0 | sed "s/.*\///"`

if [[ $# == 1 ]]; then
    VPC=$1
    SERVER=$VPC"Server"

else
    echo "Usage: $COMMAND {vpc-name}"
    exit 0
fi

# assumed is:
# 2 guest physical networks, one tagged as native, one as nuage, and operational

# also assumed offerings are tagged
# if not:
# yacc tag vpc_offering 'Default VPC offering' native
# yacc tag network_offering DefaultIsolatedNetworkOfferingForVpcNetworks native
# yacc tag network_offering NuageIsolatedNetOffering nuage

# real test case

$YACC create vpc --sync $VPC \'Default VPC offering\' 10.10.0.1/20

$YACC create network $VPC"T1" DefaultIsolatedNetworkOfferingForVpcNetworks 10.10.1.1/24 $VPC
$YACC create network $VPC"T2" DefaultIsolatedNetworkOfferingForVpcNetworks 10.10.2.1/24 $VPC

$YACC deploy virtual_machine --sync $SERVER"1" $VPC"T1"
$YACC deploy virtual_machine --sync $SERVER"2" $VPC"T2"

$YACC migrate vpc --sync $VPC NuageVpcOffering $VPC"T1"=NuageVpcTierOffering,$VPC"T2"=NuageVpcTierOffering


# $YACC migrate vpc --sync $NETWORK DefaultIsolatedNetworkOfferingWithSourceNatService

# $YACC destroy virtual_machine --sync $SERVER
# $YACC delete network --sync $NETWORK
