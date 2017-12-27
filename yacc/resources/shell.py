from __future__ import print_function
import os
import sys

from base import Base
from client import BadRequest


def _d(verb):
    # past-presence of a verb  (i know it is not complete, but for now ok)
    return (verb + 'ed' if verb[-1] in 'yt' else
            verb + 'ped' if verb[-1] == 'p'else
            verb + 'd')


def _is_set(flags, flag):
    return flag in flags and flag


class Shell(Base):

    SYNC = '--sync'
    ASYNC = '--async'
    DEEP = '--deep'
    TABLE = '-t'

    def __init__(self, resources):
        super(Shell, self).__init__()
        self.resources = resources
        self.title = resources.title()
        self.is_success = True
        self.last_created_resource = None

    def failed(self):
        self.is_success = False

    def success(self):
        return self.is_success

    def on_success(self, _):
        if self.is_success:
            print(_)

    @staticmethod
    def define_until_completion(args, default=None):
        until_c = default
        if len(args) > 1:
            if args[1] == Shell.SYNC:
                del args[1]
                until_c = True
            elif args[1] == Shell.ASYNC:
                del args[1]
                until_c = False
            elif args[1] == 'sync':  # old style
                Shell.fail('Bad request', 'Please use --sync')
        return until_c

    @staticmethod
    def human_id(entity, name=None, default=None):
        if not entity or not isinstance(entity, dict):
            return default if default else '(N/A)'
        elif name or 'name' in entity:
            return (name or entity['name']) + (
                ' (' + entity['id'] + ')' if 'id' in entity else '')
        elif 'ipaddress' in entity:
            return entity['ipaddress'] + (
                ' (' + entity['id'] + ')' if 'id' in entity else '')
        elif 'id' in entity:
            return entity['id']
        else:
            return default  # entity

    def fail(self, error, text):
        self.echo('{}: {}'.format(error, text))
        self.failed()

    def _process_entity(self, entity=None, verb='screw', synchronous=True,
                        until_completion=None, short_duration=True,
                        log_passwords=True, deep_delete=False, **kwargs):
        self.trace('_process_entity: {} {}'.format(verb, entity))
        try:
            name = None
            is_create = entity is None
            if synchronous:
                until_completion = True
            spoken_verb = (kwargs['spoken_as'] if 'spoken_as' in kwargs
                           else verb)

            if synchronous and not is_create:
                response = self.resources.execute(verb, entity)
            else:
                if deep_delete or until_completion and not short_duration:
                    print('{} in progress...'.format(spoken_verb.capitalize()))

                if is_create:
                    name = kwargs['name'] if 'name' in kwargs else None
                    if synchronous:
                        response = self.resources.create(**kwargs)
                    else:
                        response = self.resources.create(
                            until_completion=until_completion, **kwargs)
                    self.last_created_resource = response

                elif deep_delete:  # fixme
                    response = self.resources.deep_delete(entity)

                else:
                    response = self.resources.execute_async(
                        verb, entity, until_completion, **kwargs)

            print('{} {} {}{}.'.format(
                self.title, self.human_id(response, name, entity),
                '' if until_completion else 'is being ',  _d(spoken_verb)))

            if until_completion and self.has_attr(response, 'password'):
                print('The password is: {}'.format(response['password']))
                if log_passwords and name:
                    self.log_password(name, response['password'])

            if verb == 'destroy' and log_passwords:
                self.rm_password_log(entity)

        except BadRequest as e:
            self.fail(e.error, e.errortext)
        return self

    @staticmethod
    def log_password(name, password):
        with open(name + '.pass', 'w') as f:
            f.write(password)

    @staticmethod
    def rm_password_log(name):
        filename = name + '.pass'
        if os.path.exists(filename):
            os.remove(filename)

    def create(self, verb='create', short_duration=True, **kwargs):
        return self._process_entity(verb=verb,
                                    short_duration=short_duration, **kwargs)

    def create_async(self, verb='create', short_duration=True, **kwargs):
        return self._process_entity(verb=verb, synchronous=False,
                                    short_duration=short_duration, **kwargs)

    def deploy(self, return_entity=True, **kwargs):
        self.create_async('deploy', **kwargs)
        return self.last_created_resource if return_entity else self

    def acquire(self, **kwargs):
        return self.create_async('acquire', **kwargs)

    def print_entity(self, entity, table_format=False):
        self.print_entities([entity], table_format)

    def print_entities(self, entities, table_format=False):
        try:
            entity = None
            resolved_entities = []
            if entities and entities[0] == 'table':
                table_format = True
                entities.pop(0)
            for entity in entities:
                entity = self.resources.get(entity)
                if entity:
                    resolved_entities.append(entity)
            if table_format:
                self.print_all(resolved_entities)
            else:
                if len(resolved_entities) > 1:
                    self.pprint(resolved_entities)
                elif len(resolved_entities) == 1:
                    self.pprint(entity)  # avoid [ ] print

        except BadRequest as e:
            self.fail(e.error, e.errortext)

    MAX_PRINT_SIZE = 80  # will add ... if more

    def print_all(self, entities=None, filter_dict=None):

        try:
            parsed_attributes = [
                'id', 'name', 'instancename',
                'provider',
                'hostname',
                'username', 'password',
                'systemvmtype',
                # 'linklocalip', 'privateip',
                'publicip',
                'cidr',  # vpc
                'ipaddress', 'gateway', 'netmask',
                'startip', 'endip',
                'associatedvpcname', 'vpcname', 'vpcid',
                'associatednetworkname', 'networkname', 'networkid',
                'network',  # vpc tiers
                'guestnetworkname',  # router
                'issourcenat',
                'isolationmethods', 'vlan',
                'virtualmachinename', 'nic',
                'traffictype', 'cidrlist',
                'protocol', 'startport', 'endport',
                'action',
                'state', 'status', 'isready',
                'underlay',  # nuageunderlayvlanipranges
                'cpus', 'cpus_used',
                'system_vms', 'routers', 'instances',
                'value',
                'port', 'apiversion', 'cmsid'
            ]

            printed_attributes = [
                'id', 'name', 'instancename',
                'provider',
                'hostname',
                'username', 'password',
                'systemvmtype',
                # 'linklocalip', 'privateip',
                'publicip',
                'cidr',
                'ipaddress',  # ?
                # gateway, netmask
                'iprange',  # startip, endip
                'vpc',  # associatedvpcname, vpcname, vpcid
                'network',  # associatednetworkname, networkname, networkid,
                #           # guestnetwork
                'networks',  # vpc tiers
                'sourcenat',  # issourcenat
                'isolationmethods', 'vlan',
                'virtualmachinename', 'nics',  # nic
                'traffictype', 'cidrlist',
                'protocol', 'startport', 'endport',
                'action',
                'state', 'status', 'isready',
                'underlay',  # nuageunderlayvlanipranges
                'cpus', 'cpus_used',
                'system_vms', 'routers', 'instances',
                'value',
                'port', 'apiversion', 'cmsid'
            ]

            table = []

            # define content
            for r in reversed(entities or self.resources.list(filter_dict)):
                have_name = False
                have_vpcname = have_networkname = None
                gateway = start_ip = None
                row = {}
                for f in parsed_attributes:
                    if f in r and r[f] != 'N/A':
                        if f == 'name':
                            have_name = True
                        elif f == 'instancename' and not self.debug_enabled():
                            continue
                        elif f == 'username' and have_name:
                            continue
                        elif f == 'startip':
                            start_ip = r[f]
                            continue
                        elif f == 'gateway':
                            gateway = r[f]
                            continue
                        elif f in ['vpcname', 'associatedvpcname']:
                            row['vpc'] = '{}'.format(r[f])
                            have_vpcname = r[f]
                            continue
                        elif f in ['networkname', 'associatednetworkname']:
                            row['network'] = '{}'.format(r[f])
                            have_networkname = r[f]
                            continue

                        #   --------

                        if f == 'nic':
                            row['nics'] = ', '.join('{}: {}'.format(
                                net['networkname'] if 'networkname' in net
                                else 'N/A',
                                net['ipaddress'] if 'ipaddress' in net
                                else 'N/A') for net in r[f])
                        elif f == 'vpcid':
                            if not have_vpcname:  # e.g. i-don't-know
                                self.trace('(resolving...) ', end='')
                                self.disable_logging()
                                vpc = self.resolve_vpc_id(r[f])
                                self.enable_logging()
                                if vpc:
                                    row['vpc'] = '{}'.format(vpc['name'])
                        elif f == 'networkid':
                            if not have_networkname:  # e.g. fw rules
                                self.trace('(resolving...) ', end='')
                                self.disable_logging()
                                net = self.resolve_network_id(r[f])
                                self.enable_logging()
                                if net:
                                    row['network'] = '{}'.format(net['name'])
                        elif f == 'guestnetworkname':
                            row['network'] = r[f]
                        elif f == 'network':
                            row['networks'] = ','.join(
                                n['name'] for n in r[f])
                        elif f == 'netmask':
                            assert gateway
                            prefixlen = self.to_prefix_len(r[f])
                            row['cidr'] = '{}/{}'.format(gateway, prefixlen)
                        elif f == 'endip':
                            ip_range = self.compose_ip_range(start_ip, r[f])
                            row['iprange'] = '{}'.format(ip_range)
                        elif f == 'issourcenat':
                            row['sourcenat'] = 'sourcenat' if r[f] else ''
                        elif f in ['system_vms', 'routers', 'instances']:
                            row[f] = ','.join(e for e in r[f])
                        else:
                            row[f] = '{}'.format(r[f])

                table.append(row)

            if not table:
                return self

            # define column widths
            column_widths = {}
            for key in printed_attributes:
                for row in table:
                    value = row.get(key)
                    if value is not None:
                        if len(value) > self.MAX_PRINT_SIZE:
                            value = value[:(self.MAX_PRINT_SIZE - 3)] + '...'
                            row[key] = value
                        if key not in column_widths:
                            column_widths[key] = max(len(key), len(value))
                        else:
                            column_widths[key] = max(column_widths[key],
                                                     len(value))

            # define border line
            border_line = ''
            for key in printed_attributes:
                if key in column_widths:
                    column_width = column_widths[key]
                    border_line += '+-{}-'.format('-' * column_width, end='')
            border_line += '+'

            # print table
            # 1. header
            print(border_line)
            for key in printed_attributes:
                if key in column_widths:
                    column_width = column_widths[key]
                    column_format = '| {{0: <{}}} '.format(column_width)
                    print(column_format.format(key), end='')
            print('|')
            print(border_line)

            # 2. content
            for row in table:
                for key in printed_attributes:
                    if key in column_widths:
                        column_width = column_widths[key]
                        column_format = '| {{0: <{}}} '.format(column_width)
                        column_value = row.get(key) or ''
                        print(column_format.format(column_value), end='')
                print('|')

            # 3. footer
            print(border_line)

        except BadRequest as e:
            self.fail(e.error, e.errortext)
        return self

    def print_capacity(self):
        try:
            self.print_all(self.resources.get_capacity())

        except BadRequest as e:
            self.fail(e.error, e.errortext)

    def get(self, attribute):
        args = sys.argv
        f = os.path.basename(args[0])

        if len(args) == 2:
            try:
                print('{} retrieved as: {}'.format(
                    attribute, self.resources.request(
                        'get' + attribute, args[1])))
            except BadRequest as e:
                self.fail(e.error, e.errortext)
        else:
            print('Usage: {} {{{}}} '.format(f, self.resources.entity_l))
        return self

    def reset(self, attribute, response_attribute, log_passwords=True):
        args = sys.argv
        f = os.path.basename(args[0])

        if len(args) == 2:
            try:
                reset_attribute = self.resources.reset_attribute(
                    args[1], attribute)[response_attribute]

                print('{} reset to: {}'.format(
                    response_attribute, reset_attribute))

                if log_passwords and 'password' in attribute.lower():
                    self.log_password(args[1], reset_attribute)

            except BadRequest as e:
                self.fail(e.error, e.errortext)
        else:
            print('Usage: {} {{{}}} '.format(f, self.resources.entity_l))
            self.failed()
        return self

    def update(self, **kwargs):
        try:
            self.resources.update(**kwargs)

        except BadRequest as e:
            self.fail(e.error, e.errortext)

    def update_class_attribute(self):
        args = sys.argv
        f = os.path.basename(args[0])

        if len(args) == 3:
            self.resources.update_class_attribute(args[1], args[2])
            print('{} {} updated to: {}'.format(self.resources.entity,
                                                args[1], args[2]))
        else:
            print('Usage: '
                  '{} {{name}} {{value}}'.format(f))
            self.failed()
        return self

    def list(self, table_format=False):
        args = sys.argv
        f = os.path.basename(args[0])

        if len(args) > 1:
            if args[1] in {'-h', '--help'}:
                print('Usage: {} [-t] [{{id or name}}]*'.format(f))
                self.failed()
            else:
                args.pop(0)
                if len(args) == 2 and args[0] == self.DEEP:
                    self.show(args[1])

                else:
                    if len(args) > 1 and args[0] == self.TABLE:
                        args.pop(0)
                        table_format = True
                    self.print_entities(args, table_format)
        else:
            self.print_all()  # always table format, specifier is ignored
        return self

    def list_by_parent(self, parent):
        try:
            self.print_all(self.resources.list_by_parent(parent))

        except BadRequest as e:
            self.fail(e.error, e.errortext)

    def show(self, entity):
        # hack ; need to to fix this as now we put rendering logic in resources
        try:
            self.resources.show(entity)

        except BadRequest as e:
            self.fail(e.error, e.errortext)

    @staticmethod
    def compose_ip_range(start, end):
        delimiter = ' - '
        qs = start.split('.')
        qe = end.split('.')
        if qs[2] == qe[2]:
            return '.' + qs[3] + delimiter + '.' + qe[3]
        else:
            return ('.' + qs[2] + '.' + qs[3] + delimiter +
                    '.' + qe[2] + '.' + qe[3])

    @staticmethod
    def resolve_vpc_id(vpc_id):
        from resources import VPCs
        return VPCs().get(vpc_id, is_uuid=True, none_on_not_found=True)

    @staticmethod
    def resolve_network_id(net_id):
        from resources import Networks
        return Networks().get(net_id, is_uuid=True, none_on_not_found=True)

    def _process(self, verb, synchronous=False, **kwargs):
        args = sys.argv
        f = os.path.basename(args[0])
        options = self.SYNC
        if verb == 'delete' and self.resources.deep_delete_supported():
            options += '|'
            options += self.DEEP

        if (len(args) < 2 or
                len(args) > 1 and args[1] == 'sync' or  # old habits
                len(args) == 2 and args[1] in {'-h', '--help'}):
            print('Usage: {} [{}] {{entity}}*'.format(f, options))
            self.failed()
        else:
            deep_delete = verb == 'delete' and args[1] == self.DEEP
            until_completion = deep_delete or args[1] == self.SYNC
            for c in range(1 + int(until_completion), len(args)):
                self._process_entity(args[c], verb, synchronous,
                                     synchronous or until_completion,
                                     deep_delete=deep_delete,  # hacky, fixme
                                     **kwargs)
        return self

    def restart_network(self):
        args = sys.argv
        f = os.path.basename(args[0])

        if len(args) < 2 or len(args) == 2 and args[1] in {'-h', '--help'}:
            self.failed()
        else:
            until_completion = args[1] == self.SYNC
            if until_completion:
                if len(args) == 4 and args[3] == 'cleanup':
                    self._process_entity(args[2], 'restart', False,
                                         True, cleanup=True)
                elif len(args) == 3:
                    self._process_entity(args[2], 'restart', False,
                                         True, cleanup=False)
                else:
                    self.failed()
            else:
                if len(args) == 3 and args[2] == 'cleanup':
                    self._process_entity(args[1], 'restart', False,
                                         False, cleanup=True)
                elif len(args) == 2:
                    self._process_entity(args[1], 'restart', False,
                                         False, cleanup=False)
                else:
                    self.failed()

        if not self.success():
            print('Usage: {} [--sync] {{network}} [cleanup]'.format(f))
        return self

    def start(self):
        return self._process('start')

    def stop(self, forced=False):
        return self._process('stop', forced=forced)

    def restart(self):
        return self._process('restart')

    def reboot(self):
        return self._process('reboot')

    def delete(self):
        return self._process('delete')

    def delete_sync(self):
        return self._process('delete', synchronous=True)

    def destroy(self):
        return self._process('destroy', expunge=True)

    def expunge(self):
        return self._process('expunge')

    def release(self):
        return self._process('disassociate', spoken_as='release')  # mind ...

    def associate(self, **kwargs):
        try:
            self.resources.associate(**kwargs)
            print('{} associated.'.format(self.title))
        except BadRequest as e:
            self.fail(e.error, e.errortext)
        return self

    def disassociate(self, **kwargs):
        try:
            until_completion = kwargs.get('until_completion')
            self.resources.disassociate(**kwargs)
            print('{} {}disassociated.'.format(
                self.title, '' if until_completion else 'is being '))
        except BadRequest as e:
            self.fail(e.error, e.errortext)
        return self

    def register(self, **kwargs):
        try:
            self.resources.register(**kwargs)
            print('{} registered.'.format(self.title))
        except BadRequest as e:
            self.fail(e.error, e.errortext)
        return self

    def migrate(self, **kwargs):
        until_completion = kwargs.get('until_completion')
        if until_completion:
            print('Migrating...')
        try:
            self.resources.migrate(**kwargs)
            print('{} {}migrated.'.format(
                self.title, '' if until_completion else 'is being '))
        except BadRequest as e:
            self.fail(e.error, e.errortext)
        return self
