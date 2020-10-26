
# Copyright 2020, Stefan Valouch (svalouch) <svalouch@valouch.com>
# SPDX-License-Identifier: GPL-3.0-only

'''
Definition of settings classes.
'''

# pylint: disable=too-few-public-methods

from typing import Optional
from pydantic import BaseSettings, DirectoryPath


class SLMonSettings(BaseSettings):
    '''
    Daemon application settings. Most of this is used by the daemon only.
    '''

    #: Address of the Solar-Log™ device.
    solarlog_address: str
    #: Whether or not to log in. Most data is not available if this is `False`.
    solarlog_use_login: bool = True
    #: Username to log in, chose from ``user``, ``admin`` or ``installer``.
    solarlog_login_user: Optional[str] = 'user'
    #: Password to use for logging in.
    solarlog_login_password: Optional[str]
    #: Name of the Solar-Log™ device, used to identify it in the write plugins
    solarlog_name: str = 'sl1'
    #: Timezone name, the timezone can't be extracted from Solar-Log™ without logging in.
    solarlog_timezone_name: str = 'Europe/Berlin'

    #: Enables the Prometheus application monitoring endpoint.
    enable_prometheus_monitoring: bool = True
    #: Enables exposing the data via the Prometheus monitoring endpoint.
    enable_prometheus: bool = False
    #: Port at which the Prometheus endpoint listenes.
    prom_port: int = 8081

    #: Enables dumping the received data to the filesystem for later analysis.
    enable_dump: bool = False
    #: Directory where to dump the data to.
    dump_dir: Optional[DirectoryPath]

    #: Enables pushing received data to a PostgreSQL database
    enable_postgres: bool = False
    #: Database host
    pg_host: str = '127.0.0.1'
    #: Database port
    pg_port: int = 5432
    #: Database name
    pg_db: str = 'solarlog'
    #: Database user
    pg_user: str = 'postgres'
    #: Database user password
    pg_pass: str = 'postgres'

    #: Enables pushing the received data to an InfluxDB database
    enable_influx: bool = False
    #: Influx host
    influx_host: str = '127.0.0.1'
    #: Influx port
    influx_port: int = 8086
    #: Influx username
    influx_user: str = 'solarlog'
    #: Influx password
    influx_pass: str = 'solarlog'
    #: Influx database name
    influx_db: str = 'solarlog'

    class Config:
        '''
        Meta configuration
        '''
        env_prefix = 'SLMON_'
