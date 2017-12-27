#!/bin/bash

if [[ $CS_CLIENT_TRACE ]]; then
echo "Debug is already on as Trace is on."
elif [[ $CS_CLIENT_DEBUG ]]; then
echo "Debug is already on."
else
echo "To turn on debug logging, give:"
echo "export CS_CLIENT_DEBUG=True"
fi
