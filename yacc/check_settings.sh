#!/bin/bash
# show settings
set|grep CS_API
echo

if [[ $CS_CLIENT_TRACE ]]; then
echo "Trace is on. To turn off, give:"
echo "export CS_CLIENT_TRACE="
elif [[ $CS_CLIENT_DEBUG ]]; then
echo "DEBUG is on. To turn off, give:"
echo "export CS_CLIENT_DEBUG="
else
echo "To turn on debug logging, give:"
echo "export CS_CLIENT_DEBUG=True"
fi
