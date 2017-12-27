#!/bin/bash
$YACCDIR/update_configuration.py vm.allocation.algorithm firstfitleastconsumed 1>/dev/null
$YACCDIR/update_configuration.py pool.storage.allocated.capacity.disablethreshold 1 1>/dev/null

echo "System optimized. Restart management server(s)."
echo "Possibly via:"
echo "sudo systemctl restart cloudstack-management.service"
