#!/bin/bash

COMMAND=`echo $0 | sed "s/.*\///"`

IP='[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

if [[ $# == 1 ]]; then
    DEPLOYMENT_NAME=$1
    PAUSE='sleep 3'

elif [[ $# == 2 && $1 == '--dryrun' ]]; then
    DRYRUN=True
    DEPLOYMENT_NAME=$2
    YACC="echo yacc"

else
    echo "Usage: $COMMAND [--dryrun] {vpc name}"
    exit 0
fi

if [[ ! $DEPLOYMENT_SCHEMA ]];then
echo "Please source your application template first."
exit 0
fi

if [[ $DRYRUN ]];then
printf "\n${GREEN}DRY-RUNNING $DEPLOYMENT_SCHEMA: $DEPLOYMENT_NAME$NC\n"
else
printf "\n${GREEN}DEPLOYING $DEPLOYMENT_SCHEMA: $DEPLOYMENT_NAME$NC\n"
fi

if [[ $DEPLOYMENT_TYPE == 'VPC' ]];then
VPC_NAME=$DEPLOYMENT_NAME
VPC_TIER1_NAME=$VPC_NAME$VPC_TIER1_NAME
VPC_TIER2_NAME=$VPC_NAME$VPC_TIER2_NAME
VPC_TIER3_NAME=$VPC_NAME$VPC_TIER3_NAME
else
NETWORK_NAME=$DEPLOYMENT_NAME
fi


function heading {
    printf "\n${GREEN}# --- $1 ---${NC}\n"
}

function heading_red {
    printf "\n${RED}# --- $1 ---${NC}\n"
}


function heading_blue {
    printf "\n${BLUE}# --- $1 ---${NC}\n"
}


function wait_until_running {
    printf 'servers running: 0/'$2
    if [[ ! $DRYRUN ]];then while true; do
        nbr=`$YACC list virtual_machines | grep $1 | grep -c Running`
        printf '\b\b\b'$nbr'/'$2

        if [[ $nbr == $2 ]]; then
            break
        else
            $PAUSE
        fi
    done; fi
    printf '\n'
}
