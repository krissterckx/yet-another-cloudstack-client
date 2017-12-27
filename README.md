# Yet Another CloudStack Client

### Concept

With a minimum of code, this 'Yet Another CloudStack Client' (YACC) provides
useful python client classes and shell executables for basic CloudStack operations.


### Sample use

```bash
$ ./list_networks.py
8a5526e8-dd46-41c0-9d19-27c01ff86ef8 native_net Implemented

$ ./deploy_virtual_machine.py
VirtualMachine with id = 47ffeef4-697d-45ea-8d79-3482b71b8fec being deployed.

$ ./list_virtual_machines.py
91ba6e60-8fef-4c18-896f-df99405f8a8a vm1 Running
47ffeef4-697d-45ea-8d79-3482b71b8fec DEV-47ffeef4-697d-45ea-8d79-3482b71b8fec Starting
```

### To Do

- Pip packaging
- Further extensions
