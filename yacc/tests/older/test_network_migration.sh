#!/bin/bash

COMMAND=`echo $0 | sed "s/.*\///"`

if [[ $# == 1 ]]; then
    NETWORK=$1
    SERVER=$NETWORK"Server"

else
    echo "Usage: $COMMAND {network-name}"
    exit 0
fi

# assumed is:
# 2 guest physical networks, one tagged as native, one as nuage, and operational

# also assumed offerings are tagged
# if not:
# yacc tag network_offering DefaultIsolatedNetworkOfferingWithSourceNatService native
# yacc tag network_offering NuageIsolatedNetOffering nuage

# real test case
$YACC create network $NETWORK DefaultIsolatedNetworkOfferingWithSourceNatService 10.10.1.1/24
$YACC deploy virtual_machine --sync $SERVER $NETWORK

$YACC migrate network --sync $NETWORK NuageIsolatedNetOffering

$YACC migrate network --sync $NETWORK DefaultIsolatedNetworkOfferingWithSourceNatService

$YACC destroy virtual_machine --sync $SERVER
$YACC delete network --sync $NETWORK
