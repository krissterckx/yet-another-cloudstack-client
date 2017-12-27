#!/bin/bash

$YACCDIR/register_ssh_key.py kris_key "$(cat ~/.ssh/id_rsa.pub)"
