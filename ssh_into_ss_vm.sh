sudo ssh -i /root/.ssh/id_rsa.cloud -p 3922 `./yacc/list_system_vms.py s-1-VM | grep linklocalip | grep -oE "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*"`
