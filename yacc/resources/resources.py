# import base64
import time

from base import Base
from client import ClientFactory
from exception import BadRequest
from settings import Settings


class Resources(Base):
    CREATE = 'create'
    GET = 'get'
    LIST = 'list'
    UPDATE = 'update'
    DELETE = 'delete'
    MIGRATE = 'migrate'
    REBOOT = 'reboot'
    RESTART = 'restart'
    RESET = 'reset'
    START = 'start'
    STOP = 'stop'
    QUERY_JOB = 'queryAsyncJobResult'

    IDENTIFY_BY_NAME = False

    JOB_STATUS_PENDING = 0
    JOB_STATUS_SUCCESS = 1
    JOB_POLLING_DEFAULT = 2  # in seconds

    def __init__(self, default_filter=None, client=None, entity=None,
                 exit_on_bad_request=False):
        super(Resources, self).__init__()
        self.entities = self.__class__.__name__
        self.entity = entity or self.to_singular(self.entities)
        self.entity_l = self.entity.lower()
        self.default_filter = default_filter or {}
        self.client = client or ClientFactory().new_client()
        self.exit_on_bad_request = exit_on_bad_request

    @staticmethod
    def to_singular(plural):
        if plural[-1:] != 's':
            return plural
        elif plural[-4:] == 'sses':  # like 'addresses'
            return plural[:-2]
        else:
            return plural[:-1]

    def title(self):
        return self.entity

    def get_uuid(self, entity, or_any=False, sounds_like=False,
                 verify_exists=False, none_on_not_found=False):
        if entity:
            if 'id' in entity:
                return entity['id']
            elif not verify_exists and self.is_uuid(entity):
                return entity
            else:
                entity = self.get(entity, is_uuid=False,
                                  sounds_like=sounds_like,
                                  none_on_not_found=none_on_not_found)
                return entity['id'] if entity else None
        assert or_any
        first = self.first(none_on_not_found=none_on_not_found)
        return first['id'] if first else None

    def get_async_uuid(self, job, default=None):
        return self.query_job(job).get('jobinstanceid', default)

    def get_ip_uuid(self, ip, ip_key='ipaddress', none_on_not_found=False):
        if self.is_uuid(ip):
            return ip
        else:
            entity = self.get_by_key(ip_key, ip)
            if entity:
                return entity['id']
            elif none_on_not_found:
                return None
            else:
                self.no_such_entity(ip)

    def get_ip(self, ip, ip_field='ipaddress'):
        _ip = self.to_ip(ip)
        if _ip:
            return _ip
        else:
            return self.get(ip, is_uuid=True)[ip_field]

    def snd_rcv(self, cmd, args=None, entity=None, output=False):
        if args is None:
            args = {}
        if self.trace_enabled():
            self.log('Requesting {}'.format(cmd))
            self.pprint(args)
        elif self.debug_enabled():
            self.log('Requesting {} {}'.format(cmd, args))

        response = self.client.request(cmd, args, self.exit_on_bad_request)

        if output:
            self.pprint(response)
        elif self.trace_enabled():
            self.log('Received {}'.format(cmd))
            self.pprint(response)

        entity = entity or self.entity_l
        if response and entity in response:
            return response[entity]
        else:
            return response or []

    def request(self, verb, entity=None, is_uuid=None, data=None,
                asynchronous=False, until_completion=None):
        if not data:
            data = {}
        if entity and self.IDENTIFY_BY_NAME:
            data['name'] = entity
        elif entity:
            if self.has_attr(entity, 'id'):
                entity = entity['id']
            elif is_uuid is False or (not is_uuid and
                                      not self.is_uuid(entity)):
                entity = self.get_uuid(entity)
            data['id'] = entity
        response = self.snd_rcv(verb, data)
        # leave 'assert' separated into 2 cases as it benefits troubleshooting
        if asynchronous:
            assert self.is_job(response)  # async. job in reality is sync.
            return self.asynchronous(response, until_completion)
        else:
            # synchronous
            assert not self.is_job(response)  # sync. job in reality is async.
            return response

    def request_entity(self, verb, entity=None, is_uuid=None, data=None,
                       asynchronous=False, until_completion=None):
        return self.request(verb + self.entity, entity, is_uuid, data,
                            asynchronous, until_completion)

    def request_entities(self, verb, data=None, entities=None, entity=None):
        if entities and not entity:
            entity = self.to_singular(entities).lower()
        return self.snd_rcv(verb + (entities or self.entities), data, entity)

    def create_entity(self, resource, asynchronous=False,
                      until_completion=None):
        return self.request_entity(self.CREATE, data=resource,
                                   asynchronous=asynchronous,
                                   until_completion=until_completion)

    def create(self, resource):
        # use synchronous method by default (!), but can be overruled to async.
        return self.create_entity(resource)

    # there is no create_async for above-mentioned reason

    def list_all(self):
        return self.request_entities(self.LIST)

    def list(self, filter_dict=None, add_default_filter=True):
        return self.list_entities(filter_dict, add_default_filter)

    def list_by_parent(self, parent):
        pass

    def list_entities(self, filter_dict, add_default_filter,
                      entities=None, entity=None):
        if filter_dict and add_default_filter:
            filter_dict.update(self.default_filter)
        return self.request_entities(
            self.LIST, filter_dict or self.default_filter, entities, entity)

    def get(self, entity=None, by=None, is_uuid=None, sounds_like=False,
            none_on_not_found=False):
        items = None
        if entity is None:
            self.debug('Get {} unspecified.'.format(self.entity))
            items = self.list()
        elif is_uuid is not False and (is_uuid or self.is_uuid(entity)):
            self.debug('Get {} by uuid {}.'.format(self.entity, entity))
            items = self.list({'id': entity})
        else:
            by = by or 'name'
            if sounds_like:
                self.debug('Get {} by sounds_like {}.'.format(
                    self.entity, entity))
                for item in self.list():
                    if entity.lower() in item[by].lower():
                        return item
            else:
                item = self.get_by_key(by, entity,
                                       none_on_not_found)
                if item:
                    return item
        if items:
            return items[0]
        #   not found
        elif none_on_not_found:
            return None
        #   else
        self.no_such_entity(entity or 'query')

    def get_by_key(self, key, value, none_on_not_found=False):
        self.debug('Get {} by {} {}.'.format(self.entity, key, value))
        for item in self.list():
            if item[key] == value:
                return item
        if none_on_not_found:
            return None
        #   else:
        self.no_such_entity(value)

    def get_or_none(self, entity=None, sounds_like=False):
        return self.get(entity, sounds_like=sounds_like,
                        none_on_not_found=True)

    def query_job(self, job):
        return self.snd_rcv(self.QUERY_JOB, {'jobid': job['jobid']})

    def query_until_completion(self, job, polling=None):
        polling = polling or self.JOB_POLLING_DEFAULT
        while True:
            time.sleep(polling)
            job = self.query_job(job)
            if job.get('jobstatus') != self.JOB_STATUS_PENDING:
                break
        return self.check_job(job)

    def asynchronous(self, job, until_completion=None):
        self.trace('Asynchronous request{}...'.format(
            'until comppletion' if until_completion else ''))
        if until_completion is None:
            until_completion = Settings().get_until_completion()
        if until_completion:
            job = self.query_until_completion(job)
            if 'jobresult' in job:
                job_result = job['jobresult']
                if self.entity_l in job_result:
                    return job_result[self.entity_l]
                elif 'success' in job_result:  # deleteVPC
                    return job_result['success']
            return job
        else:
            return {'id': (job.get('jobinstanceid') or
                           job.get('id') or  # createVPC job adds vpc id
                           self.get_async_uuid(job, job['jobid']))}

    @staticmethod
    def is_job(job):
        return job and 'jobid' in job

    def check_job(self, job):
        if job['jobstatus'] != Resources.JOB_STATUS_SUCCESS:
            self.server_error(job['jobresult'])
        return job

    def no_such_entity(self, entity):
        raise BadRequest('{} {} could not be found.'.format(
            self.entity, entity))

    def no_unique_entity(self, entity):
        raise BadRequest('{} {} is not unique, please use id.'.format(
            self.entity, entity))

    def show(self, entity):
        raise BadRequest('No show implemented for {}.'.format(self.entity))

    @staticmethod
    def server_error(job_result):
        assert job_result and isinstance(job_result, dict)
        raise BadRequest('Server error: {} {}'.format(
            job_result.get('errorcode', 'N/A'),
            job_result.get('errortext', 'N/A')))

    def first(self, none_on_not_found=True):
        return self.get(none_on_not_found=none_on_not_found)

    def get_attribute(self, entity, attribute):
        # can't use request_entity as this is about the attribute
        return self.request(self.GET + attribute, entity)

    def reset_attribute(self, entity, attribute, asynchronous=True):
        # can't use request_entity as this is about the attribute
        return self.request(
            self.RESET + attribute, entity, asynchronous=asynchronous,
            until_completion=True)

    def update(self, entity=None, **kwargs):
        asynchronous = False
        until_completion = None
        if 'asynchronous' in kwargs:
            asynchronous = kwargs['asynchronous']
            kwargs.pop('asynchronous')
        if 'until_completion' in kwargs:
            until_completion = kwargs['until_completion']
            kwargs.pop('until_completion')
        return self.request_entity(
            self.UPDATE, entity=entity, data=kwargs, asynchronous=asynchronous,
            until_completion=until_completion)

    def update_class_attribute(self, name, value):
        return self.request_entity(
            self.UPDATE, data={'name': name, 'value': value})

    # syntactical sugar
    def execute(self, verb, entity, **kwargs):
        return self.request_entity(verb, entity, data=kwargs)

    def execute_async(self, verb, entity, until_completion=None,
                      **kwargs):
        return self.request_entity(
            verb, entity, data=kwargs, asynchronous=True,
            until_completion=until_completion)

    def enable(self, entity, enable=True, asynchronous=False):
        if asynchronous:
            return self.execute_async(
                self.UPDATE, entity, until_completion=True,
                state='enabled' if enable else 'disabled')
        else:
            return self.execute(
                self.UPDATE, entity, state='enabled' if enable else 'disabled')

    def restart(self, entity, until_completion=None):
        return self.execute_async(self.RESTART, entity, until_completion)

    def delete(self, entity, until_completion=None):
        return self.execute_async(self.DELETE, entity, until_completion)

    def delete_sync(self, entity, deep=False):
        if deep:
            return self.deep_delete(entity)
        else:
            return self.execute(self.DELETE, entity)

    @staticmethod
    def deep_delete_supported():
        return False

    def deep_delete(self, entity):
        raise BadRequest('No deep delete implemented for {}.'.format(
            self.entity))


class Configurations(Resources):
    pass


class Zones(Resources):
    pass


class NuageVspDevices(Resources):
    def list_by_parent(self, phys_net):
        return self.list(
            {'physicalnetworkid': PhysicalNetworks().get_uuid(phys_net)})

    def update(self, phys_net=None, username=None, password=None):
        phys_net = PhysicalNetworks().get_uuid(phys_net)
        super(NuageVspDevices, self).update(physicalnetworkid=phys_net,
                                            username=username,
                                            password=password,
                                            asynchronous=True,
                                            until_completion=True)


class Hosts(Resources):
    HOSTS_METRICS = 'HostsMetrics'

    def __init__(self, client=None):
        super(Hosts, self).__init__({'type': 'routing'}, client)

    # added for convenience but not that useful
    def list_metrics(self):
        return self.snd_rcv(self.LIST + self.HOSTS_METRICS, {})

    def get_capacity(self):
        hosts = []
        system_vms = SystemVms().list()
        routers = Routers().list()
        instances = VirtualMachines().list()
        for host in self.list():
            cpus_used = 0
            host_capacity = {
                'hostname': host['name'],
                'cpus': host['cpunumber'],
                'system_vms': [],
                'routers': [],
                'instances': []
            }
            for system_vm in system_vms:
                if system_vm.get('hostid') == host['id']:
                    host_capacity['system_vms'].append(system_vm['name'])
                    cpus_used += 1
            for router in routers:
                if router.get('hostid') == host['id']:
                    host_capacity['routers'].append(router['name'])
                    cpus_used += 1
            for instance in instances:
                if instance.get('hostid') == host['id']:
                    host_capacity['instances'].append(instance['name'])
                    cpus_used += int(instance['cpunumber'])
            host_capacity['cpus_used'] = cpus_used
            hosts.append(host_capacity)
        return hosts


class Accounts(Resources):
    pass


class SSHKeyPairs(Resources):
    REGISTER = 'register'
    IDENTIFY_BY_NAME = True

    def register(self, name, public_key):
        data = {
            'name': name,
            'publickey': public_key
        }
        return self.request_entity(self.REGISTER, data=data)


class Domains(Resources):
    pass


class Users(Resources):
    REGISTER_USER_KEYS = 'registerUserKeys'

    def register_user_keys(self, user='admin', by='username'):
        keys = self.request(
            self.REGISTER_USER_KEYS, self.get(user, by=by))['userkeys']
        return self.client.update_keys(keys['apikey'], keys['secretkey'])


class Offerings(Resources):
    def create_helper(self, offering, supported_services, enable,
                      void_if_already_exists=True,
                      asynchronous=False, until_completion=None):
        offering['supportedservices'] = ','.join(supported_services.keys())
        idx = 0
        for service, provider in supported_services.items():
            offering['serviceproviderlist[%d].service' % idx] = service
            offering['serviceproviderlist[%d].provider' % idx] = provider
            idx += 1

        try:
            offering = self.create_entity(
                offering, asynchronous=asynchronous,
                until_completion=until_completion)
        except BadRequest as e:
            if void_if_already_exists and 'already exists' in e.errortext:
                return {'name': offering['name']}
            else:
                raise

        if offering and enable:
            self.enable(offering['id'], asynchronous=asynchronous)

        return offering


class NetworkOfferings(Offerings):
    def create(self, keyword, name=None, for_vpc=False, enable=True,
               user_data=True, skip_if_exists=False):
        shared = False
        if keyword == 'isolated':
            proposed_name = ('VpcTierOffering' if for_vpc
                             else 'IsolatedNetOffering')
            connectivity = 'VpcVirtualRouter' if for_vpc else 'VirtualRouter'
            user_data_provider = connectivity

        elif keyword == 'isolated_configdrive':
            proposed_name = ('VpcTierOfferingWithConfigDrive' if for_vpc
                             else 'IsolatedNetOfferingWithConfigDrive')
            connectivity = 'VpcVirtualRouter' if for_vpc else 'VirtualRouter'
            user_data_provider = 'ConfigDrive'

        elif keyword == 'shared':
            if for_vpc:
                raise BadRequest('Shared network cannot be a VPC tier.')
            proposed_name = 'SharedNetOffering'
            connectivity = 'VirtualRouter'
            user_data_provider = connectivity
            shared = True

        elif keyword == 'shared_configdrive':
            if for_vpc:
                raise BadRequest('Shared network cannot be a VPC tier.')
            proposed_name = 'SharedNetOfferingWithConfigDrive'
            connectivity = 'VirtualRouter'
            user_data_provider = 'ConfigDrive'
            shared = True

        elif keyword == 'nuage_isolated':
            proposed_name = ('NuageVpcTierOffering' if for_vpc
                             else 'NuageIsolatedNetOffering')
            user_data_provider = ('VpcVirtualRouter' if for_vpc
                                  else 'VirtualRouter')
            connectivity = 'NuageVsp'

        elif keyword == 'nuage_isolated_configdrive':
            proposed_name = ('NuageVpcTierOfferingWithConfigDrive' if for_vpc
                             else 'NuageIsolatedNetOfferingWithConfigDrive')
            user_data_provider = 'ConfigDrive'
            connectivity = 'NuageVsp'

        elif keyword == 'nuage_shared':
            if for_vpc:
                raise BadRequest('Shared network cannot be a VPC tier.')
            proposed_name = 'NuageSharedNetOffering'
            user_data_provider = 'VirtualRouter'
            shared = True
            connectivity = 'NuageVsp'

        elif keyword == 'nuage_shared_configdrive':
            if for_vpc:
                raise BadRequest('Shared network cannot be a VPC tier.')
            proposed_name = 'NuageSharedNetOfferingWithConfigDrive'
            user_data_provider = 'ConfigDrive'
            shared = True
            connectivity = 'NuageVsp'

        else:
            raise BadRequest('Bad keyword {}.'.format(keyword))

        if not user_data:
            proposed_name += 'Basic'
        name = name or proposed_name
        if skip_if_exists:
            net_off = NetworkOfferings().get(name, none_on_not_found=True)
            if net_off is not None:
                return net_off

        supported_services = {
            'dhcp': connectivity,
        }
        if user_data:
            supported_services['userdata'] = user_data_provider
        if connectivity == 'NuageVsp':
            supported_services['connectivity'] = connectivity
        if not shared:
            # supported_services['dns'] = 'VirtualRouter'
            supported_services['sourcenat'] = connectivity
            supported_services['staticnat'] = connectivity
            if for_vpc:
                supported_services['networkacl'] = connectivity
            else:
                supported_services['firewall'] = connectivity

        offering = {
            'name': name,
            'displaytext': name,
            'forvpc': for_vpc,
            'traffictype': 'guest',
            'guestiptype': 'shared' if shared else 'isolated'
        }
        if for_vpc:
            offering['ispersistent'] = True  # most logical choice
            offering['conservemode'] = False
        elif shared:
            offering['specifyvlan'] = False  # Nuage has foreseen ability to
            #                                              set this to False
            offering['specifyipranges'] = True  # must be True for Shared off.
            offering['ispersistent'] = False  # must be False for Shared off.
            if connectivity == 'NuageVsp':
                offering['servicecapabilitylist[0].service'] = \
                    'Connectivity'
                offering['servicecapabilitylist[0].provider'] = connectivity
                offering['servicecapabilitylist[0].capabilitytype'] = \
                    'PublicAccess'
                offering['servicecapabilitylist[0].capabilityvalue'] = 'True'

        # else:  # isolated net
        #   offering['ispersistent'] = False  # most logical choice

        return self.create_helper(offering, supported_services, enable)
        # (network offerings are created synchronously)


class VPCOfferings(Offerings):
    def create(self, keyword, name=None, enable=True, skip_if_exists=False,
               user_data=True, until_completion=None):
        if keyword == 'nuage':
            proposed_name = 'NuageVpcOffering'
            user_data_provider = 'VpcVirtualRouter'
        elif keyword == 'nuage_configdrive':
            proposed_name = 'NuageVpcOfferingWithConfigDrive'
            user_data_provider = 'ConfigDrive'
        else:
            raise BadRequest('Bad keyword {}.'.format(keyword))
        if not user_data:
            proposed_name += 'Basic'
        name = name or proposed_name
        if skip_if_exists:
            vpc_off = VPCOfferings().get(name, none_on_not_found=True)
            if vpc_off is not None:
                return vpc_off

        supported_services = {
            'connectivity': 'NuageVsp',
            'dhcp': 'NuageVsp',
            'sourcenat': 'NuageVsp',
            'staticnat': 'NuageVsp',
            'networkacl': 'NuageVsp'
        }
        if user_data:
            supported_services['userdata'] = user_data_provider
        offering = {
            'name': name,
            'displaytext': name,
            'ispersistent': True
        }
        return self.create_helper(offering, supported_services, enable,
                                  asynchronous=True,
                                  until_completion=until_completion)


class ServiceOfferings(Resources):
    pass


class Templates(Resources):
    def __init__(self, client=None):
        super(Templates, self).__init__({'templatefilter': 'all'}, client)


class Networks(Resources):

    def create(self, name, display=None,
               offering='DefaultIsolatedNetworkOfferingWithSourceNatService',
               cidr=None, vpc=None, acl=None, zone=None, **kwargs):
        network = {
            'name': name,
            'displaytext': display or name,
            'networkofferingid': NetworkOfferings().get_uuid(offering),
            'zoneid': Zones().get_uuid(zone, or_any=True)
        }
        if cidr:
            cidr = self.to_network(cidr)
            network['gateway'] = str(cidr.ip)
            network['netmask'] = str(cidr.netmask)
        if vpc:
            network['vpcid'] = VPCs().get_uuid(vpc)
            if not cidr:
                raise BadRequest('VPC tiers require a CIDR.')
        if acl:
            network['aclid'] = NetworkACLLists().get_uuid(acl)

        network.update(**kwargs)

        return self.create_entity(network)  # (networks-create is synchronous!)

    @staticmethod
    def deep_delete_supported():
        return True

    def deep_delete(self, network):
        network = Networks().get(network)
        vms = VirtualMachines().list(
            filter_dict={'networkid': network['id']})
        for vm in vms:
            VirtualMachines().destroy(vm, until_completion=True)
        Networks().delete(network, until_completion=True)

    def migrate(self, network=None, offering=None, resume=False,
                until_completion=None):
        data = {
            'networkid': Networks().get_uuid(network),
            'networkofferingid': NetworkOfferings().get_uuid(offering),
            'resume': resume
        }
        # note: as of nature of migrateNetwork response, even when
        # no until_completion is requested, one job query will be done
        return self.request_entity(self.MIGRATE, data=data,
                                   asynchronous=True,
                                   until_completion=until_completion)


class VPCs(Resources):

    def create(self, name, display=None,
               offering='Default VPC offering', cidr=None, zone=None,
               until_completion=None):
        vpc = {
            'name': name,
            'displaytext': display or name,
            'vpcofferingid': VPCOfferings().get_uuid(offering),
            'cidr': cidr,  # 'super cidr'
            'zoneid': Zones().get_uuid(zone, or_any=True)
        }
        return self.create_entity(vpc, True, until_completion)

    def show(self, vpc):
        vpc = self.get(vpc)
        vpc_offering = VPCOfferings().get(vpc['vpcofferingid'], is_uuid=True)
        self.echo('\n   VPC: %s  (%s)' % (vpc['name'], vpc_offering['name']))
        net_count = len(vpc['network'])
        cnt = 0
        for network in vpc['network']:
            network = Networks().get(network['id'])
            is_last = cnt == net_count - 1
            cnt += 1
            self.echo('      |')
            self.echo('      +->Network: %s' % network['name'])

            vms = VirtualMachines().list(
                filter_dict={'networkid': network['id']})
            if len(vms) > 0:
                self.echo('      %s         |' % (' ' if is_last else '|'))
            for vm in vms:
                if vm.get('publicip'):
                    public_ip = ' (public: %s)' % vm['publicip']
                else:
                    public_ip = ''
                self.echo('      %s         +->Server: %s (%s)%s' % (
                    ' ' if is_last else '|',
                    vm['name'], vm['nic'][0]['ipaddress'], public_ip))

    @staticmethod
    def deep_delete_supported():
        return True

    def deep_delete(self, vpc):
        vpc = self.get(vpc)
        for network in vpc['network']:
            network = Networks().get(network['id'])
            vms = VirtualMachines().list(
                filter_dict={'networkid': network['id']})
            for vm in vms:
                VirtualMachines().destroy(vm, until_completion=True)
            Networks().delete(network, until_completion=True)
        VPCs().delete(vpc, until_completion=True)

    def migrate(self, vpc=None, offering=None, network_offerings=None,
                resume=False, until_completion=None):
        data = {
            'vpcid': VPCs().get_uuid(vpc),
            'vpcofferingid': VPCOfferings().get_uuid(offering),
            'resume': resume
        }
        idx = 0
        for net, net_off in network_offerings.items():
            data['tiernetworkofferings[%d].networkid' % idx] = \
                Networks().get_uuid(net)
            data['tiernetworkofferings[%d].networkofferingid' % idx] = \
                NetworkOfferings().get_uuid(net_off)
            idx += 1
        # note: as of nature of migrateVPC response, even when
        # no until_completion is requested, one job query will be done
        return self.request_entity(self.MIGRATE, data=data,
                                   asynchronous=True,
                                   until_completion=until_completion)


class PhysicalNetworks(Resources):
    pass


class VirtualMachines(Resources):
    CREATE = 'deploy'
    DELETE = 'destroy'
    EXPUNGE = 'expunge'

    VM_PASSWORD = 'VMPassword'
    PASSWORD_FOR_VM = 'PasswordForVirtualMachine'

    PASSWORD = 'password'

    COREOS_CLOUDINIT_JSON = \
        '{"ignition":{"config":{},"timeouts":{},"version":"2.1.0"},"networkd' \
        '":{},"passwd":{"users":[{"name":"core","sshAuthorizedKeys":["ssh-rs' \
        'a AAAAB3NzaC1yc2EAAAADAQABAAABAQDhRBpESFb7SvvPrwns67li4nXEP0uBuTj6p' \
        'PSy08uqxMKw64a40bWsehm0A7+cAnf8i67Qyd9Zcl7nhBe5KDoTEVTzMk8rSVM5UIVg' \
        'TORIF02kpnSYw9ko/9YLuROGDKTKiqTnllFhEP8PcqCMZ34anNjfwRwqxU0ANFpPtSY' \
        'sNsBTa5IlyTkfa9OqBL9SDKXpM1xnHlGMyqP0wEyYRqdXPdxN1alXNLblWJFDhZIWEJ' \
        'jptrmnulbu5zYhS0lNfbeNS0E/0uFViZQNvBMMklXu4RQrIpWdTwI8h4LkEAJquRrGb' \
        'AiIWVpN3sXlXrssfAHuweg+BJ0DBFslKIETGpOf"]}]},"storage":{},"systemd"' \
        ':{"units":[{"contents":"[Unit]\nDescription=Formats the ephemeral d' \
        'rive\nAfter=dev-vda.device\nRequires=dev-vda.device\n[Service]\nTyp' \
        'e=oneshot\nRemainAfterExit=yes\nExecStart=/usr/sbin/wipefs -f /dev/' \
        'vda\nExecStart=/usr/sbin/mkfs.ext4 -F /dev/vda\n","enabled":true,"n' \
        'ame":"format-ephemeral.service"},{"contents":"[Unit]\nDescription=M' \
        'ount ephemeral to /var/lib/docker\nRequires=format-ephemeral.servic' \
        'e\nAfter=format-ephemeral.service\n[Mount]\nWhat=/dev/vda\nWhere=/v' \
        'ar/lib/docker\nType=ext4\n","enabled":true,"name":"var-lib-docker.m' \
        'ount"},{"dropins":[{"contents":"[Service]\nEnvironment=\"HTTP_PROXY' \
        '=http://proxy.lbs.alcatel-lucent.com:8000/\"\nEnvironment=\"HTTPS_P' \
        'ROXY=http://proxy.lbs.alcatel-lucent.com:8000/\"\n","name":"50-http' \
        '-proxy.conf"},{"contents":"[Unit]\nAfter=var-lib-docker.mount\nRequ' \
        'ires=var-lib-docker.mount\n","name":"10-wait-docker.conf"}],"name":' \
        '"docker.service"}]}}'

    # hacky, clean me up
    COREOS_INJECTION_SSH_KEYPAIR_KRIS = \
        'eyJpZ25pdGlvbiI6eyJjb25maWciOnt9LCJ0aW1lb3V0cyI6e30sInZlcnNpb24iOiI' \
        'yLjEuMCJ9LCJuZXR3b3JrZCI6e30sInBhc3N3ZCI6eyJ1c2VycyI6W3sibmFtZSI6Im' \
        'NvcmUiLCJzc2hBdXRob3JpemVkS2V5cyI6WyJzc2gtcnNhIEFBQUFCM056YUMxeWMyR' \
        'UFBQUFEQVFBQkFBQUJBUURoUkJwRVNGYjdTdnZQcnduczY3bGk0blhFUDB1QnVUajZw' \
        'UFN5MDh1cXhNS3c2NGE0MGJXc2VobTBBNytjQW5mOGk2N1F5ZDlaY2w3bmhCZTVLRG9' \
        'URVZUek1rOHJTVk01VUlWZ1RPUklGMDJrcG5TWXc5a28vOVlMdVJPR0RLVEtpcVRubG' \
        'xGaEVQOFBjcUNNWjM0YW5OamZ3UndxeFUwQU5GcFB0U1lzTnNCVGE1SWx5VGtmYTlPc' \
        'UJMOVNES1hwTTF4bkhsR015cVAwd0V5WVJxZFhQZHhOMWFsWE5MYmxXSkZEaFpJV0VK' \
        'anB0cm1udWxidTV6WWhTMGxOZmJlTlMwRS8wdUZWaVpRTnZCTU1rbFh1NFJRcklwV2R' \
        'Ud0k4aDRMa0VBSnF1UnJHYkFpSVdWcE4zc1hsWHJzc2ZBSHV3ZWcrQkowREJGc2xLSU' \
        'VUR3BPZiJdfV19LCJzdG9yYWdlIjp7fSwic3lzdGVtZCI6eyJ1bml0cyI6W3siY29ud' \
        'GVudHMiOiJbVW5pdF1cbkRlc2NyaXB0aW9uPUZvcm1hdHMgdGhlIGVwaGVtZXJhbCBk' \
        'cml2ZVxuQWZ0ZXI9ZGV2LXZkYS5kZXZpY2VcblJlcXVpcmVzPWRldi12ZGEuZGV2aWN' \
        'lXG5bU2VydmljZV1cblR5cGU9b25lc2hvdFxuUmVtYWluQWZ0ZXJFeGl0PXllc1xuRX' \
        'hlY1N0YXJ0PS91c3Ivc2Jpbi93aXBlZnMgLWYgL2Rldi92ZGFcbkV4ZWNTdGFydD0vd' \
        'XNyL3NiaW4vbWtmcy5leHQ0IC1GIC9kZXYvdmRhXG4iLCJlbmFibGVkIjp0cnVlLCJu' \
        'YW1lIjoiZm9ybWF0LWVwaGVtZXJhbC5zZXJ2aWNlIn0seyJjb250ZW50cyI6IltVbml' \
        '0XVxuRGVzY3JpcHRpb249TW91bnQgZXBoZW1lcmFsIHRvIC92YXIvbGliL2RvY2tlcl' \
        'xuUmVxdWlyZXM9Zm9ybWF0LWVwaGVtZXJhbC5zZXJ2aWNlXG5BZnRlcj1mb3JtYXQtZ' \
        'XBoZW1lcmFsLnNlcnZpY2VcbltNb3VudF1cbldoYXQ9L2Rldi92ZGFcbldoZXJlPS92' \
        'YXIvbGliL2RvY2tlclxuVHlwZT1leHQ0XG4iLCJlbmFibGVkIjp0cnVlLCJuYW1lIjo' \
        'idmFyLWxpYi1kb2NrZXIubW91bnQifSx7ImRyb3BpbnMiOlt7ImNvbnRlbnRzIjoiW1' \
        'NlcnZpY2VdXG5FbnZpcm9ubWVudD1cIkhUVFBfUFJPWFk9aHR0cDovL3Byb3h5Lmxic' \
        'y5hbGNhdGVsLWx1Y2VudC5jb206ODAwMC9cIlxuRW52aXJvbm1lbnQ9XCJIVFRQU19Q' \
        'Uk9YWT1odHRwOi8vcHJveHkubGJzLmFsY2F0ZWwtbHVjZW50LmNvbTo4MDAwL1wiXG4' \
        'iLCJuYW1lIjoiNTAtaHR0cC1wcm94eS5jb25mIn0seyJjb250ZW50cyI6IltVbml0XV' \
        'xuQWZ0ZXI9dmFyLWxpYi1kb2NrZXIubW91bnRcblJlcXVpcmVzPXZhci1saWItZG9ja' \
        '2VyLm1vdW50XG4iLCJuYW1lIjoiMTAtd2FpdC1kb2NrZXIuY29uZiJ9XSwibmFtZSI6' \
        'ImRvY2tlci5zZXJ2aWNlIn1dfX0='

    def deploy(self, name, networks=None, offering='small', template='centos',
               zone=None, keypair=None, until_completion=None):
        assert networks
        net_ids = ','.join(
            Networks().get_uuid(net, or_any=True) for net in networks)
        vm = {
            'name': name,
            'zoneid': Zones().get_uuid(zone, or_any=True),
            'networkids': net_ids,
            'serviceofferingid': ServiceOfferings().get_uuid(
                offering, sounds_like=True),
            'templateid': Templates().get_uuid(template, sounds_like=True)
        }
        if keypair:
            if template == 'coreos':
                # hack - set user data thru injection
                vm['userdata'] = self.COREOS_INJECTION_SSH_KEYPAIR_KRIS
                # base64.encodestring(self.COREOS_CLOUDINIT_JSON)
            else:
                vm['keypair'] = keypair

        # gimmick
        # if template != 'coreos':
        #   userdata = '#!/bin/bash\necho \'Powered by CloudStack\'>/etc/motd'
        #   vm['userdata'] = base64.encodestring(userdata)

        return self.create_entity(vm, True, until_completion)

    def create(self, name, networks=None, offering='small', template='centos',
               zone=None, keypair=None, until_completion=None):
        return self.deploy(name, networks, offering, template, zone,
                           keypair, until_completion)

    def get_password(self, vm):
        return self.get_attribute(self.VM_PASSWORD, vm)

    def reset_password(self, vm):
        return self.reset_attribute(self.PASSWORD_FOR_VM, vm)[self.PASSWORD]

    def start(self, vm, until_completion=None):
        return self.execute_async(self.START, vm, until_completion)

    def reboot(self, vm, until_completion=None):
        return self.execute_async(self.REBOOT, vm, until_completion)

    def stop(self, vm, forced=False, until_completion=None):
        return self.execute_async(self.STOP, vm, until_completion,
                                  forced=forced)

    def expunge(self, vm, until_completion=None):
        return self.execute_async(self.EXPUNGE, vm, until_completion)

    def destroy(self, entity, expunge=True, until_completion=None):
        return self.execute_async(self.DELETE, entity, until_completion,
                                  expunge=expunge)


class SystemVms(Resources):
    pass


class Routers(Resources):
    def __init__(self, client=None):
        super(Routers, self).__init__({'listall': 'true'}, client)


class VlanIpRanges(Resources):
    def create(self, cidr, start_ip=None, end_ip=None, network=None,
               vlan=None, zone=None):
        cidr = self.to_network(cidr)
        start_ip = start_ip or cidr[2]  # TODO(me) this is in assumption
        #                                 gateway is set to 1st ip
        end_ip = end_ip or cidr[-1]
        ip_range = {
            'gateway': str(cidr.ip),
            'netmask': str(cidr.netmask),
            'startip': start_ip,
            'endip': end_ip
        }
        if network:
            # the use case is adding ip-range to a shared network
            ip_range['forvirtualnetwork'] = False
            ip_range['networkid'] = Networks().get_uuid(network)

        else:
            # the use case is adding a public ip-range
            ip_range['forvirtualnetwork'] = True
            ip_range['zoneid'] = Zones().get_uuid(zone, or_any=True)
            ip_range['vlan'] = 'untagged'
            # physical network is auto-chosen for to be the one supporting
            # public traffic type
        if vlan:
            ip_range['vlan'] = vlan
        return self.create_entity(ip_range)['vlan']  # synchronously
        # (entity is called 'vlan' in create response)


class NuageUnderlayVlanIpRanges(Resources):
    ENTITY = 'NuageVlanIpRange'

    def __init__(self, default_filter=None, client=None, _=None):
        super(NuageUnderlayVlanIpRanges, self).__init__(
            default_filter, client, self.ENTITY)


class IpAddresses(Resources):
    ALTER_EGO = 'PublicIpAddresses'

    ACQUIRE = 'associate'  # associate to account ... (yes, confusing)
    ENABLE_STATIC_NAT = 'enableStaticNat'
    DISABLE_STATIC_NAT = 'disableStaticNat'
    RELEASE = 'disassociate'  # disassociate from account ... (yes, again)
    DELETE = RELEASE

    def title(self):
        return 'PublicIp'

    def acquire(self, network=None, vpc=None, network_or_vpc=None,
                zone=None, domain=None, vm=None, until_completion=None):
        data = {
            'zoneid': Zones().get_uuid(zone, or_any=True),
            'domainid': Domains().get_uuid(domain, or_any=True)
        }
        if network:
            data['networkid'] = Networks().get_uuid(network)
        elif vpc:
            data['vpcid'] = VPCs().get_uuid(vpc)
        elif network_or_vpc:
            network = Networks().get(network_or_vpc,
                                     none_on_not_found=True)
            if network:
                if network.get('vpcid'):
                    self.echo('Network is part of vpc: acquiring to vpc.')
                    data['vpcid'] = network['vpcid']
                data['networkid'] = network['id']
            else:
                data['vpcid'] = VPCs().get_uuid(network_or_vpc)
        else:
            raise BadRequest('Must specify network or vpc.')

        ip = self.request_entity(
            self.ACQUIRE, data=data, asynchronous=True,
            until_completion=until_completion)['ipaddress']
        return self.associate(ip, vm) if vm else ip

    def create(self, network=None, vpc=None, network_or_vpc=None,
               zone=None, domain=None, vm=None, until_completion=None):
        return self.acquire(network, vpc, network_or_vpc, zone, domain,
                            vm, until_completion)

    def list(self, filter_dict=None, add_default_filter=True):
        return self.list_entities(
            filter_dict, add_default_filter, entities=self.ALTER_EGO)

    def get(self, ip=None, by=None, is_uuid=None, sounds_like=False,
            none_on_not_found=False):
        if not is_uuid:
            ip = self.get_ip_uuid(ip, none_on_not_found=none_on_not_found)
            if ip is None:
                return None
        return super(IpAddresses, self).get(
            ip, is_uuid=True, sounds_like=sounds_like,
            none_on_not_found=none_on_not_found)

    def associate(self, ip, vm, tier=None):
        ip = self.get(ip)
        tier_is_uuid = None
        vm = VirtualMachines().get(vm)
        if ip.get('vpcid'):
            tier = vm['nic'][0]['networkid']
            tier_is_uuid = True
        data = {
            'ipaddressid': ip['id'],
            'virtualmachineid': vm['id']
        }
        if tier:
            data['networkid'] = (tier if tier_is_uuid else
                                 Networks().get_uuid(tier))
        self.request(self.ENABLE_STATIC_NAT, data=data)
        return ip

    def disassociate(self, ip, until_completion=None):
        data = {
            'ipaddressid': self.get_ip_uuid(ip)
        }
        return self.request(self.DISABLE_STATIC_NAT, data=data,
                            asynchronous=True,
                            until_completion=until_completion)

    # convenience
    def release(self, ip, until_completion=False):
        return self.delete(ip, until_completion)


class NetworkACLLists(Resources):

    def create(self, name=None, description=None, vpc=None):
        acl_list = {
            'name': name,
            'vpcid': VPCs().get_uuid(vpc)
        }
        if description:
            acl_list['description'] = description
        return self.create_entity(acl_list, True)


class NetworkACLs(Resources):

    def create(self, acl_list=None, cidr=None, protocol=None, port=None):
        if not cidr:
            cidr = '0.0.0.0/0'
        else:
            self.check_cidr(cidr)
        if protocol == 'icmp':
            acl = {
                'aclid': NetworkACLLists().get_uuid(acl_list),
                'cidrlist': cidr,
                'code': '-1',
                'type': '-1',
                'protocol': protocol
            }
        else:
            acl = {
                'aclid': NetworkACLLists().get_uuid(acl_list),
                'cidrlist': cidr,
                'startport': port,
                'endport': port,
                'protocol': protocol
            }
        return self.create_entity(acl, True)


class FirewallRules(Resources):

    def create(self, ip_address=None, cidr=None, protocol=None, port=None):
        if not cidr:
            cidr = '0.0.0.0/0'
        else:
            self.check_cidr(cidr)
        if protocol == 'icmp':
            fw_rule = {
                'ipaddressid': IpAddresses().get_uuid(ip_address),
                'cidrlist': cidr,
                'code': '-1',
                'type': '-1',
                'protocol': protocol
            }
        else:
            fw_rule = {
                'ipaddressid': IpAddresses().get_uuid(ip_address),
                'cidrlist': cidr,
                'startport': port,
                'endport': port,
                'protocol': protocol
            }
        return self.create_entity(fw_rule, True)

    def list_by_ip(self, ip):
        return self.list({'ipaddressid': IpAddresses().get_ip_uuid(ip)})
