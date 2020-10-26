
# Copyright 2020, Stefan Valouch (svalouch) <svalouch@valouch.com>
# SPDX-License-Identifier: GPL-3.0-only

'''
Client implementation for interfacing with a Solar-Log™ device.
'''

import json
import logging
from datetime import datetime
from json import JSONDecodeError
from typing import Dict, Optional

import requests

from .dumper import Dumper
from .exceptions import SolarLogError

log = logging.getLogger('slmon.solarlogclient')


class SolarLogClient:
    '''
    Represents the Solar-Log™ device. Provides a abstraction of the device and provides session handling.

    :param username: The username to log in (e.g. `user`)
    :param password: The password to log in
    :param host: The host to connect to
    :param login: Whether to log in and try to maintain a session.
    :param dumper: Optional dumper that, when set, dumps the retrieved data as soon as possible.
    '''

    _username: Optional[str]
    _password: Optional[str]
    _host: str
    _schema: str

    _s: requests.Session
    _logged_in: bool
    #: Session token
    _token: str
    _dumper: Optional[Dumper]

    _login_url: str
    _getjp_url: str

    # data obtained from the device

    _sl_revision: Optional[int]

    # logcheck
    _sl_logcheck_logged_in: int
    _sl_logcheck_login_level: int
    _sl_logcheck_access_level: int

    _timeout = (5, 5)

    # pylint: disable=too-many-arguments
    def __init__(self, host: str, login: bool, username: Optional[str] = None, password: Optional[str] = None,
                 dumper: Optional[Dumper] = None) -> None:
        self._username = username
        self._password = password
        self._host = host
        self._login = login
        self._token = ''
        self._dumper = dumper
        self._sl_revision = None

        self._s = requests.Session()

        self._schema = 'http'
        self._login_url = f'{self._schema}://{self._host}/login'
        self._getjp_url = f'{self._schema}://{self._host}/getjp'

        self.init_session()

    def dump(self, filename: str, data: str) -> None:
        '''
        If the dumper is available, hands of the data to be dumped.

        :param filename: The name of the file to dump into. The dumper adds a timestamp and the json extension on it
           own.
        :param data: The data to dump.
        '''
        if self._dumper:
            self._dumper.dump(filename, data)

    @property
    def sl_revision(self) -> int:
        '''
        Returns the Solar-Log™ revision. If the revision has not been queried before, performs a query.

        :raises SolarLogError: If the query for the revision failed.
        '''
        if not self._sl_revision:
            return self.get_revision()
        return self._sl_revision

    def set_login(self, login: bool) -> None:
        '''
        Controls whether the client tries to log in before the next request if it detects that it is not logged in.
        This can be set to `False` before accessing the Solar-Log™ with a webbrowser as it does not allow more than one
        active session and the client would kick the user out of the session each time it is called.
        '''
        self._login = login

    @property
    def login(self) -> bool:
        '''
        Returns whether the client performs a login if it detects that its session has ended.
        '''
        return self._login

    @property
    def logged_in(self) -> bool:
        '''
        Returns whether the client thinks that its session is valid. This value is updated on querying the data logger.
        '''
        return self._logged_in

    def init_session(self) -> None:
        '''
        Initializes the requests session
        '''
        self._logged_in = False
        self._s.cookies.set('banner_hidden', 'false')

    def init_data(self) -> None:
        '''
        Initializes internal data structures, should be called after a reconnect.
        '''
        self._sl_revision = None
        self._sl_logcheck_logged_in = 0
        self._sl_logcheck_login_level = 0
        self._sl_logcheck_access_level = 0

    def do_login(self) -> bool:
        '''
        Performs the login action. Updates the internal `_logged_in` value and returns whether it was successful.

        :return: Whether it was successful.
        '''
        log.debug(f'do_login _login: {self._login} _logged_in: {self._logged_in}')
        if self._username is None or self._password is None:
            log.error('Can\'t log in, username and/or password not set')
        elif self._login:
            if self._logged_in:
                self.handle_logout()

            log.info(f'Performing login as user "{self._username}"')
            login_resp = self._s.post(self._login_url, data={'u': self._username, 'p': self._password},
                                      timeout=self._timeout)
            if login_resp.status_code != 200:
                log.warning(f'Login failed: {login_resp.status_code} "{login_resp.text}"')
            elif 'SUCCESS' in login_resp.text:
                log.debug(f'do_login resp: {login_resp.text} cookies: {login_resp.cookies}')
                try:
                    self._token = login_resp.cookies['SolarLog']
                except KeyError:
                    log.error('Could not find "SolarLog" cookie')
                else:
                    log.info(f'Logged in to the solarlog at {self._host}')
                    self._logged_in = True
            elif 'FAILED' in login_resp.text:
                if '(password)' in login_resp.text:
                    log.warning('Logging in failed: password')
                else:
                    log.warning(f'Logging in failed: "{login_resp.text}"')
        log.info(f'do_login: logged_in = {self._logged_in}')
        return self._logged_in

    def handle_logout(self) -> None:
        '''
        Performs the neccessary steps to return to a clean, not logged-in state. This is used when the client detects
        that the server does not consider its session valid anymore.
        '''
        log.info('Handling logout')
        self._logged_in = False
        self._token = ''

    def getjp(self, data: str) -> requests.Response:
        '''
        Low-level function to access the ``getjp`` endpoint of the Solar-Log™ device. If the JSON response contains the
        words ``ACCESS DENIED``, then the logout handler is triggered.

        :param data: The query string. If logged in, the token will automatically be prepended.
        :return: The response object.
        '''
        headers = {
            'Content-Type': 'application/json',
        }
        log.debug(f'token: {self._token}')

        if not self._logged_in:
            log.debug('getjp: not logged in')
            if self._login:
                log.debug('getjp: logging in')
                self.do_login()
                resp = self._s.post(self._getjp_url, data=f'token={self._token};{data}', headers=headers,
                                    timeout=self._timeout)
            else:
                resp = self._s.post(self._getjp_url, data=data, headers=headers, timeout=self._timeout)
        else:
            resp = self._s.post(self._getjp_url, data=f'token={self._token};{data}', headers=headers,
                                timeout=self._timeout)
        self.dump('getjp', resp.text)
        if '"ACCESS DENIED"' in resp.text:
            self.handle_logout()
        resp.raise_for_status()
        return resp

    def get_revision(self) -> int:
        '''
        Queries the device for the current revision number.
        '''
        resp = self._s.get(f'{self._schema}://{self._host}/revision.html',
                           params={'_': int(datetime.now().timestamp() * 1000)})
        if resp.status_code == 200:
            try:
                rev = int(resp.text)
            except ValueError as exc:
                msg = 'Revision: not a valid integer'
                log.error(msg)
                raise SolarLogError(msg) from exc

            if rev < 1000:
                msg = f'Revision: sanity check failed, not a valid revision: {rev}'
                log.error(msg)
                raise SolarLogError(msg)
            self._sl_revision = rev
        else:
            raise SolarLogError(f'Failed to get content: {resp.status_code} {resp.text}')
        return self._sl_revision

    def get_open_json(self) -> Dict:
        '''
        Requests the "Open JSON" output. This does not require a login. The keys are converted to integers on the fly.
        '''
        resp = self.getjp('{"801":{"100":null,"170":null}}')
        if resp.status_code != 200:
            raise SolarLogError(f'OpenJSON: Unexpected status code {resp.status_code}')
        log.debug(resp.text)
        return json.loads(resp.text, object_hook=lambda d: {
            int(k): [int(i) for i in v] if isinstance(v, list) else v for k, v in d.items()})

    def get_lcd(self) -> Dict:
        '''
        Queries for the current set of LCD data and returns the result as a dict. This function works without valid
        login.
        '''
        lcd_resp = self.getjp('{"701":null,"794":{"0":null}}')
        if lcd_resp.status_code != 200:
            raise SolarLogError(f'LCD: Unexpected status code {lcd_resp.status_code}')
        try:
            return lcd_resp.json()
        except JSONDecodeError as exc:
            raise SolarLogError(f'Could not parse json response: {str(exc)}') from exc

    def do_logcheck(self) -> None:
        '''
        Checks the login and access state. The data is stored internally.

        :raises SolarLogError: If querying failed or the data is not parseable.
        '''
        logcheck_resp = self._s.get(f'{self._schema}://{self._host}/logcheck',
                                    params={'_': int(datetime.now().timestamp() * 1000)})
        if logcheck_resp.status_code == 200:
            data = logcheck_resp.text.split(';')
            if len(data) != 3:
                raise SolarLogError(f'logcheck: got invalid data: {logcheck_resp.text}')
            self._sl_logcheck_logged_in = int(data[0])
            self._sl_logcheck_login_level = int(data[1])
            self._sl_logcheck_access_level = int(data[2])
        else:
            raise SolarLogError(f'logcheck: got unexpected status code {logcheck_resp.status_code}')
