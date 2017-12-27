#!/bin/bash
if [ -f cs.rc ];then
   . cs.rc
else
   . cs.rc.sample
fi

yacc/set_user_keys.py generate

. cs.rc

UUID=[a-zA-Z0-9_\-]*

if [[ $MARVIN_CFG_FILE && -f $MARVIN_CFG_FILE ]]; then
sudo sed -i 's/\"apiKey\": \"'$UUID'\"/\"apiKey\": \"'$CS_API_KEY'\"/' $MARVIN_CFG_FILE
sudo sed -i 's/\"securityKey\": \"'$UUID'\"/\"securityKey\": \"'$CS_API_SECRET'\"/' $MARVIN_CFG_FILE
fi
