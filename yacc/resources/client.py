import base64
import hashlib
import hmac
import json
import requests
import ssl
import urllib

from datetime import datetime
from datetime import timedelta

from requests_toolbelt import SSLAdapter

from base import Base
from exception import BadRequest

# Disable HTTPS verification warnings.
from requests.packages import urllib3

urllib3.disable_warnings()


class Client(Base):
    def __init__(self, url=None, username='admin', password='password',
                 api_key=None, secret_key=None,
                 expires=600, verifysslcert=False, signature_version=3):
        super(Client, self).__init__()
        self.url = url
        self.username = username
        self.password = password
        self.domain = '/'
        self.api_key = api_key
        self.secret_key = secret_key
        self.expires = expires
        self.verifysslcert = verifysslcert
        self.signature_version = signature_version
        self.session = None
        self.session_key = None

    def prep_args(self, command, args):
        args = args.copy() if args else {}
        args['command'] = command
        args['response'] = 'json'
        if self.signature_version >= 3:
            args['signatureversion'] = self.signature_version
            expiration_time = datetime.utcnow() + timedelta(
                seconds=int(self.expires))
            args['expires'] = expiration_time.strftime(
                '%Y-%m-%dT%H:%M:%S+0000')
        for key in args.keys():
            value = args[key]
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            args[key] = value
            if not key:
                args.pop(key)
        return args

    def update_keys(self, key, secret):
        self.api_key = key
        self.secret_key = secret
        return self.url, key, secret

    def http_request(self, http_cmd=None, args=None, **kwargs):
        if http_cmd == 'GET':
            kwargs.setdefault('allow_redirects', True)
        self.trace('HTTP %s: %s %s' % (http_cmd, self.url, args))
        return self.session.request(
            http_cmd, self.url, params=args, verify=self.verifysslcert,
            **kwargs)

    def password_login(self):
        self.debug('LOGIN with username/password')
        resp = self.request('login', {'username': self.username,
                                      'password': self.password,
                                      'domain': self.domain})

        self.session_key = resp['sessionkey']
        self.debug('LOGIN OK')

    def request(self, cmd, args,
                exit_on_bad_request=False, truncate_error=True):
        if not self.session:
            self.session = requests.Session()
            self.session.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1))

        http_cmd = 'POST' if cmd == 'login' else 'GET'
        args = self.prep_args(cmd, args)
        resp = None

        def sign_request(params, secret_key):
            self.trace('Signing request')
            request = zip(params.keys(), params.values())
            request.sort(key=lambda x: x[0].lower())
            hash_str = '&'.join(
                ['='.join(
                    [r[0].lower(),
                     urllib.quote_plus(str(r[1]), safe='*').lower()
                         .replace('+', '%20').replace('%3A', ':')]
                ) for r in request]
            )
            return base64.encodestring(hmac.new(secret_key, hash_str,
                                                hashlib.sha1).digest()).strip()

        if self.api_key:
            assert self.secret_key
            args['apikey'] = self.api_key
            args['signature'] = sign_request(args, self.secret_key)
        elif cmd != 'login':
            self.password_login()
            args['sessionkey'] = self.session_key

        try:
            resp = self.http_request(http_cmd, args)
            result = resp.text
            if resp.status_code == 200:  # success
                error = None
            elif resp.status_code == 401:  # auth issue
                error = '401 Authentication error'
            elif resp.status_code == 405:
                error = ('Method not allowed, unauthorized access on URL: %s' %
                         self.url)
            elif resp.status_code == 531:
                error = ('Error authenticating at %s using username: %s,'
                         'password: %s, domain: %s' % (self.url,
                                                       self.username,
                                                       self.password,
                                                       self.domain))
            else:
                error_msg = resp.headers.get('X-Description')
                if truncate_error:
                    error_msg = error_msg.split(': {')[0]
                error = '{0}: {1}'.format(resp.status_code, error_msg)
        except requests.exceptions.ConnectionError as e:
            raise BadRequest('Connection refused by server: %s' % e)

        except Exception as pokemon:
            result = None
            error = pokemon.message

        if error is not None:
            self.debug('Error: {}'.format(error))

        if result:
            try:
                response = json.loads(result, "utf-8")
                self.trace('RESPONSE: %s: %s' % (resp.status_code, response))
            except ValueError as e:
                self.error('Received: {}'.format(result))
                response = None
                error = e
        else:
            response = None

        if response and isinstance(response, dict):
            m = list(v for v in response.keys() if 'response' in v.lower())
            if not m:
                error = 'Invalid response received: %s' % response
            else:
                response = response[filter(
                    lambda x: 'response' in x, response.keys())[0]]

        if error:
            if exit_on_bad_request:
                self.error(error)
            else:
                raise BadRequest(error)
        else:
            return response


class MockedClient(Client):
    def __init__(self):
        super(MockedClient, self).__init__()

    def request(self, command, args, exit_on_bad_request=False):
        return 0


_client = None


class ClientFactory(Base):

    def new_client(self):
        global _client

        if _client is None:

            url = self.from_os('CS_API_ENDPOINT')
            api_key = self.from_os('CS_API_KEY')
            secret_key = self.from_os('CS_API_SECRET')

            if not url:
                if self.bool_from_os('CS_CLIENT_MOCK'):
                    self.info('INFO: '
                              'You are in mock mode as CS_API_ENDPOINT/KEY/'
                              'SECRET is not set.')
                    _client = MockedClient()
                else:
                    self.echo('Please make sure CS_API_ENDPOINT is set.')
                    self.echo('Alternatively set CS_CLIENT_MOCK to True for '
                              'trying out the software with mocked client.')
                    exit(1)
            else:
                if not api_key:
                    self.warn('no apikey/secret is configured; '
                              'slower performance can be expected.')

                _client = Client(url, api_key=api_key, secret_key=secret_key)

        return _client
