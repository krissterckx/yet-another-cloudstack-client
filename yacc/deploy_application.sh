#!/bin/bash

. $YACCDIR/utils/functions.sh

SECONDS=0

if [[ $VPC_NAME ]];then

# VPC

# create vpc
heading 'Creating VPC'
$YACC create vpc --sync $VPC_NAME $VPC_OFFERING 10.10.0.0/20

# and its tiers ...
# deploy Web tier & server
heading 'Creating Web tier ACL list'
$YACC create network_acllist $WEBACLLIST \'Secured HTTPS\' $VPC_NAME
$YACC create network_acl $WEBACLLIST 0.0.0.0/0 icmp
$YACC create network_acl $WEBACLLIST 0.0.0.0/0 tcp 22
$YACC create network_acl $WEBACLLIST 0.0.0.0/0 tcp 443  # secure https

heading 'Creating Web tier'
$YACC create network $VPC_TIER1_NAME $VPC_TIER_OFFERING 10.10.1.1/24 $VPC_NAME $WEBACLLIST

heading 'Deploying Web server(s)'
if [[ ! $NBR_WEB_SERVERS ]];then
NBR_WEB_SERVERS=1
fi
for WEB in `seq 1 $NBR_WEB_SERVERS`; do
    $YACC deploy virtual_machine $SERVER_SYNC $VPC_TIER1_NAME$WEB $VPC_TIER1_NAME $SERVER_TEMPLATE $SERVER_KEY_PAIR
    $PAUSE  # give YACC scheduler room to monitor CPU usage
done
$PAUSE  # don't delete ; it leads to issues

# deploy App tier & servers
if [[ ! $NBR_APP_SERVERS ]];then
NBR_APP_SERVERS=0
fi
if [[ $NBR_APP_SERVERS > 0 ]];then
heading 'Creating App tier ACL list'
$YACC create network_acllist $APPACLLIST \'Insecure HTTP\' $VPC_NAME
$YACC create network_acl $APPACLLIST 0.0.0.0/0 icmp
$YACC create network_acl $APPACLLIST 0.0.0.0/0 tcp 22
$YACC create network_acl $APPACLLIST 0.0.0.0/0 tcp 80   # insecure http

heading 'Creating App tier'
$YACC create network $VPC_TIER2_NAME $VPC_TIER_OFFERING 10.10.2.1/24 $VPC_NAME $APPACLLIST

heading 'Deploying App servers'
for APP in `seq 1 $NBR_APP_SERVERS`; do
    $YACC deploy virtual_machine $SERVER_SYNC $VPC_TIER2_NAME$APP $VPC_TIER2_NAME $SERVER_TEMPLATE $SERVER_KEY_PAIR
    $PAUSE  # give YACC scheduler room to monitor CPU usage
done
fi

# deploy DB tier & servers
if [[ ! $NBR_DB_SERVERS ]];then
NBR_DB_SERVERS=0
fi
if [[ $NBR_DB_SERVERS > 0 ]];then
heading 'Creating DB tier ACL list'
$YACC create network_acllist $DBACLLIST \'SQL access\' $VPC_NAME
$YACC create network_acl $DBACLLIST 0.0.0.0/0 icmp
$YACC create network_acl $DBACLLIST 0.0.0.0/0 tcp 22
$YACC create network_acl $DBACLLIST 0.0.0.0/0 tcp 3306  # mysql

heading 'Creating DB tier'
$YACC create network $VPC_TIER3_NAME $VPC_TIER_OFFERING 10.10.3.1/24 $VPC_NAME $DBACLLIST 

heading 'Deploying DB servers'
for DB in `seq 1 $NBR_DB_SERVERS`; do
    $YACC deploy virtual_machine $SERVER_SYNC $VPC_TIER3_NAME$DB $VPC_TIER3_NAME $SERVER_TEMPLATE $SERVER_KEY_PAIR
    $PAUSE  # give YACC scheduler room to monitor CPU usage
done
fi

# acquire and associate public ip to web server
heading 'Acquiring & Applying public IP to Web server'
$YACC acquire public_ip $VPC_NAME $VPC_TIER1_NAME"1"  # first web server

# wait until running
heading 'Waiting for all servers to be running'
NBR_SERVERS=$(($NBR_WEB_SERVERS + $NBR_APP_SERVERS + $NBR_DB_SERVERS))
wait_until_running $VPC_NAME $NBR_SERVERS

else

# isolated network

heading 'Creating isolated network'
$YACC create network $NETWORK_NAME $NETWORK_OFFERING 10.10.1.1/24

heading 'Deploying server(s)'
for i in `seq 1 $NBR_SERVERS`; do
$YACC deploy virtual_machine $SERVER_SYNC $NETWORK_NAME"Server"$i $NETWORK_NAME $SERVER_TEMPLATE $SERVER_KEY_PAIR
$PAUSE  # don't delete ; it leads to issues
$PAUSE  # don't delete ; it leads to issues
done

# acquire and associate public ip to the server
heading 'Acquiring & Applying public IP to server'
ipaddress='<ip>'
acquire_public_ip=`$YACC acquire public_ip $NETWORK_NAME $NETWORK_NAME"Server1"`
echo $acquire_public_ip
if [[ ! $DRYRUN ]];then
ipaddress=`echo "$acquire_public_ip" | grep -E -o $IP`
fi

# configuring FW rule to enable ssh login
heading 'Configuring Firewall rule at Public IP to open up SSH access'
$YACC create firewall_rule $ipaddress 0.0.0.0/0 tcp 22

# wait until running
heading 'Waiting for to be running'
wait_until_running $NETWORK_NAME $NBR_SERVERS
fi

# final report

if [[ ! $DRYRUN ]]; then
# minutes=$(( SECONDS / 60 ))
# round better with:
minutes=$((( $SECONDS / 60) + ($SECONDS % 60 > 0)))
echo "completed in $minutes mins."
fi

# show vpc:
# echo "cs list vpc --deep "$VPC_NAME
#
# delete vpc:
# echo "cs delete vpc --deep "$VPC_NAME
