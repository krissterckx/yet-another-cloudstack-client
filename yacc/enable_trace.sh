#!/bin/bash

if [[ $CS_CLIENT_TRACE ]]; then
echo "Trace is already on."
else
echo "To turn on trace logging, give:"
echo "export CS_CLIENT_TRACE=True"
fi
