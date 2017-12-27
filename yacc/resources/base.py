from __future__ import print_function

from exception import BadRequest

import os
import pprint
import sys

from netaddr import IPAddress
from netaddr import IPNetwork
from netaddr import core as netaddr_core
from uuid import UUID


class Base(object):

    ERROR = 1
    INFO = 2
    DEBUG = 3
    TRACE = 4

    log_level = None
    log_enabled = None

    flags = {}

    DEFAULT_PPRINT_DEPTH = 5

    def __init__(self):
        if Base.log_enabled is None:
            Base.log_enabled = True

        if Base.log_level is None:
            if self.bool_from_os('CS_CLIENT_TRACE'):
                Base.log_level = Base.TRACE
                self.trace('Trace is on.')
            elif self.bool_from_os('CS_CLIENT_DEBUG'):
                Base.log_level = Base.DEBUG
                self.debug('Debug is on.')
            else:
                Base.log_level = Base.INFO

    @staticmethod
    def set_flag(key, value):
        Base.flags[key] = value

    @staticmethod
    def get_flag(key, default=None):
        return Base.flags.get(key, default)

    @staticmethod
    def from_os(env_name, default=None):
        env_name = os.environ.get(env_name)
        return env_name if env_name else default

    @staticmethod
    def bool_from_os(env_name):
        return Base.from_os(env_name, 'f').lower()[:1] == 't'

    @staticmethod
    def debug_enabled():
        return Base.log_level >= Base.DEBUG

    @staticmethod
    def trace_enabled():
        return Base.log_level >= Base.TRACE

    @staticmethod
    def trace_level():
        return ('TRACE' if Base.trace_enabled() else
                'DEBUG' if Base.debug_enabled() else
                'INFO')

    @staticmethod
    def echo(s, end=None):
        print(s, end=end)

    @staticmethod
    def log(s, trace_level=None, end=None):
        if Base.log_enabled:
            Base.echo('[{}] {}'.format(
                trace_level or Base.trace_level(), s), end=end)

    @staticmethod
    def error(s, end=None, fatal=True):
        if fatal:
            Base.echo('ERROR: ' + s, end=end)
            Base.exit()
        else:
            Base.log(s, 'ERROR', end=end)

    @staticmethod
    def warn(s, end=None):
        Base.echo('WARN: ' + s, end=end)

    @staticmethod
    def info(s, end=None):
        Base.log(s, end=end)

    @staticmethod
    def debug(s, end=None):
        if Base.debug_enabled():
            Base.log(s, end=end)

    @staticmethod
    def trace(s, end=None):
        if Base.trace_enabled():
            Base.log(s, end=end)

    @staticmethod
    def enable_logging():
        Base.log_enabled = True

    @staticmethod
    def disable_logging():
        Base.log_enabled = False

    @staticmethod
    def has_attr(entity, attribute):
        return isinstance(entity, dict) and attribute in entity

    @staticmethod
    def pprint(obj, depth=None):
        if Base.log_enabled:
            pprint.PrettyPrinter(
                indent=4, depth=depth or Base.DEFAULT_PPRINT_DEPTH).pprint(obj)

    @staticmethod
    def is_uuid(uuid_str):
        try:
            return str(UUID(uuid_str)) == uuid_str
        except ValueError:
            return False

    @staticmethod
    def to_ip(ip):
        try:
            return str(IPAddress(ip))
        except ValueError:
            return None
        except netaddr_core.AddrFormatError:
            return None

    @staticmethod
    def to_network(cidr):
        try:
            return IPNetwork(cidr)
        except ValueError as e:
            raise BadRequest('Value error: {}'.format(e))
        except netaddr_core.AddrFormatError as e:
            raise BadRequest('Format error: {}'.format(e))

    @staticmethod
    def to_prefix_len(netmask):
        return IPAddress(netmask).netmask_bits()

    @staticmethod
    def check_ip(ip):
        try:
            IPAddress(ip)
            return True
        except ValueError:
            return None
        except netaddr_core.AddrFormatError:
            return None

    @staticmethod
    def check_cidr(cidr):
        try:
            IPNetwork(cidr)
            return True
        except ValueError:
            return None
        except netaddr_core.AddrFormatError:
            return None

    @staticmethod
    def string_input(value_name, termination=' :', default=None,
                     allow_empty=False):
        while True:
            if default:
                print('{}{} [{}] '.format(
                    value_name, termination, default), end='')
            else:
                print('{}{} '.format(value_name, termination), end='')
            value = sys.stdin.readline().strip()
            if default and not value:
                value = default
            print('\r', end='')
            # empty check
            if allow_empty or value:
                break
            else:
                print('Empty is now allowed.')

        return value

    @staticmethod
    def numerical_input(value_name, min_value, max_value, default=True,
                        default_value=None):
        if default:
            def_value = min_value if not default_value else default_value
        else:
            def_value = None
        while True:
            try:
                value = int(Base.string_input(value_name, default=def_value))
                if min_value <= value <= max_value:
                    break
            except (ValueError, NameError):
                pass
            print('Please pick a number between {} and {}.'.format(
                min_value, max_value))
        return value

    @staticmethod
    def shell_input(value_name, shell_var, default=None):
        value = Base.from_os(shell_var)
        return value if value else Base.string_input(
            value_name + ' (' + shell_var + ' is undefined)', default=default)

    @staticmethod
    def boolean_input(question, default=True):
        resp = Base.string_input(question, '? (Y/n)' if default else '? (y/N)',
                                 allow_empty=True).lower()
        return 'y' in resp if resp else default

    @staticmethod
    def exit():
        exit(0)
