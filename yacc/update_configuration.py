#!/usr/bin/python
from resources.resources import Configurations
from resources.shell import Shell

Shell(Configurations()).update_class_attribute().on_success(
    'A management server(s) restart may be necessary.')
