# prep

$YACCDIR/tag_physical_network.py Underlay native
$YACCDIR/tag_physical_network.py Nuage nuage

$YACCDIR/tag_network_offering.py DefaultIsolatedNetworkOfferingForVpcNetworks native
$YACCDIR/tag_vpc_offering.py 'Default VPC offering' native

$YACCDIR/create_network_offering.py nuage_isolated for-vpc
$YACCDIR/create_vpc_offering.py nuage
$YACCDIR/tag_network_offering.py NuageVpcTierOffering nuage
$YACCDIR/tag_vpc_offering.py NuageVpcOffering nuage

# ----

. $YACCDIR/../2tier-native.rc.sample

$YACCDIR/deploy_application.sh twotierapp

