#!/usr/bin/python
from __future__ import print_function
import os
import sys

from resources.base import Base
from resources.resources import Users

args = sys.argv
f = os.path.basename(args[0])


class KeysRegister(Base):

    def __init__(self, args):
        super(KeysRegister, self).__init__()
        if len(args) == 1:
            _, key, secret = Users().register_user_keys()
            self.echo('apikey: %s' % key)
            self.echo('secretkey: %s' % secret)

        elif len(args) <= 3 and args[1] == 'generate':
            url, key, secret = Users().register_user_keys()
            rc_filename = args[2] if len(args) == 3 else 'cs.rc'
            with open(rc_filename, 'w') as f:
                f.write('export CS_API_ENDPOINT={}\n'.format(url))
                f.write('export CS_API_KEY={}\n'.format(key))
                f.write('export CS_API_SECRET={}\n'.format(secret))
            self.echo('A new resource file has been generated.')
            self.echo('Please source it by giving:')
            self.echo('. {}'.format(rc_filename))

        else:
            self.echo(
                'Usage: %s [{{generate}}] [{{resource-filename}}]' % f)


KeysRegister(sys.argv)
