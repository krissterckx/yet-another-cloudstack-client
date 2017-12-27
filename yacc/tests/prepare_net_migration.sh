# prep

$YACCDIR/tag_physical_network.py Underlay native
$YACCDIR/tag_physical_network.py Nuage nuage

$YACCDIR/tag_network_offering.py DefaultIsolatedNetworkOfferingWithSourceNatService native

$YACCDIR/create_network_offering.py nuage_isolated
$YACCDIR/tag_network_offering.py NuageIsolatedNetOffering nuage

# ----

. $YACCDIR/../1tier-native.rc.sample

$YACCDIR/deploy_application.sh singletierapp

