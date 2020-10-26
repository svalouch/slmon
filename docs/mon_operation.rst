######################
Operation instructions
######################

The main part of the software is written as a `daemon`, intended to be started by a process manager such as OpenRC or
SystemD. Other parts are indended to be called from the shell to perform various operations.

.. _mon_operation-configuration:

Configuration
*************

The main configuration is done using environment variables. These can be set in the shell using ``export(1P)`` or
specified when calling the program.

For the curious: The settings are in ``settings.py`` in the ``SLMonSettings`` class. Turn the keys to all-upper case
and prepend ``SLMON_``.

Accessing the Solar-Log™ device
===============================

.. option:: SLMON_SOLARLOG_ADDRESS

   The network address of the Solar-Log™ data logger without schema ("http://")

.. option:: SLMON_SOLARLOG_USE_LOGIN

   Controls whether the software tries to maintain a session on the data logger.

.. option:: SLMON_SOLARLOG_LOGIN_USER

   The user used for logging in. This can be ``user``, ``admin`` or ``installer``. For most purposes, the default
   (``user``) is perfectly fine.

.. option:: SLMON_SOLARLOG_LOGIN_PASSWORD

   The clear-text password used to log in. This is only needed when `SLMON_SOLARLOG_USE_LOGIN` is ``True``.

.. option:: SLMON_SOLARLOG_NAME

   The identifier of the device, used by some of the writer methods below to allow for using the same destination for
   multiple instances. Defaults to ``sl1``.

Monitoring the application
==========================

.. option:: SLMON_ENABLE_PROMETHEUS_MONITORING

   Setting this to ``True`` (default) enables the prometheus endpoint that exposes some details about the operation of
   the software. This is used by the daemon only.

.. option:: SLMON_PROM_PORT

   The TCP port at which the prometheus endpoint listens. It binds to all IPs. Defaults to ``8081`` and is used by the
   daemon only.

Features
========

.. _mon_operation-configuration-prometheus:

Exposing data to Prometheus
---------------------------

.. option:: SLMON_ENABLE_PROMETHEUS

   Setting this to ``True`` (default: ``False``) enables exposing the data acquired from the data logger via the
   prometheus endpoint. `SLMON_ENABLE_PROMETHEUS_MONITORING` must be ``True`` for this to work. This is used by
   the daemon only.

.. _mon_operation-configuration-postgresql:

Exporting data to PostgreSQL
----------------------------

.. warning::

   The PostgreSQL writer is not in a working shape.

.. option:: SLMON_ENABLE_POSTGRES

   Setting this to ``True`` enables writing the data acquired from the data logger to a PostgreSQL database. Daemon
   only.

.. option:: SLMON_PG_HOST

   PostgreSQL host to connect to. Daemon only.

.. option:: SLMON_PG_PORT

   PostgreSQL port, defaults to 5432. Daemon only.

.. option:: SLMON_PG_DB

   PostgreSQL database to use. Defaults to ``solarlog``, daemon only.

.. option:: SLMON_PG_USER

   User used to connect to the PostgreSQL database, defaults to ``postgres``. Daemon only.

.. option:: SLMON_PG_PASS

   Password for the PostgreSQL user. Defaults to ``postgres``. Daemon only.

.. _mon_operation-configuration-influxdb:

Exporting data to InfluxDB
--------------------------
The main intention of the daemon is to export the data to an InfluxDB database.

.. option:: SLMON_ENABLE_INFLUX

   Setting this to ``True`` enables support for writing the data obtained from the data logger to an InfluxDB database.
   Used by the daemon only, as are the following InfluxDB related settings.

.. option:: SLMON_INFLUX_HOST

   Address to reach the InfluxDB.

.. option:: SLMON_INFLUX_PORT

   Port to connect to, defaults to ``8086``.

.. option:: SLMON_INFLUX_USER

   User used to connect to the InfluxDB, defaults to ``solarlog``

.. option:: SLMON_INFLUX_PASS

   Password for the InfluxDB user. Defaults to ``solarlog``

.. option:: SLMON_INFLUX_DB

   InfluxDB database to write to.

.. _mon_operation-configuration-dumper:

Dumping data
------------
The so-called Dumper can be enabled to dump everything that's received from the Solar-Log™ device to the filesystem.

.. option:: SLMON_ENABLE_DUMP

   Setting this to ``True`` enables the dumper.

.. option:: SLMON_DUMP_DIR

   An existing directory where the data will be dumped to.

.. _mon_operation-session_handling:

Session handling
****************

When ``SLMON_SOLARLOG_USE_LOGIN`` is set to ``True``, the software will maintain a session on the data logger and will
perform a login whenever it detects that its session has become invalid. This means that the web frontend of the
data logger will seize to function for all other purposes that require a login.

In order to enable endusers to log into the data logger themselves without completely interrupting data collection (the
Open JSON data can be acquired without a valid session), the software can be sent signals to change the state of
``SLMON_SOLARLOG_USE_LOGIN`` on the fly while it is running.

Send a ``SIGUSR1`` to the software to disable the refresh of the session and send ``SIGUSR2`` to enable it.

If one wants to log in, simply run ``kill -USR1 <pid of slmon>`` and the software will not create a new session when it
detects that its session has become invalid. The software will note in the log:

::

   2020-08-27 22:58:30,287 - slmon.daemon - INFO - Caught SIGUSR1, disabling login

However, it will still send its session cookie with each request. If the session stays valid, it will get all the data
it normally would. Once the session ends because a user logged in to the data logger from another device, its session
ends, which it will mention like so:

::

   2020-08-27 23:01:24,942 - slmon.solarlogclient - INFO - Handling logout

Fron then on, it will only query the Open JSON format until it receives the signal to log in again. The data loggers
web interface can be used as normal. When done, execute ``kill -USR2 <pid of slmon>`` and it will log:

::

   2020-08-27 23:02:57,464 - slmon.daemon - INFO - Caught SIGUSR2, enabling login

On the next request, it will perform a login and maintain its session.

Running the daemon
******************
As stated above, the configuration is done using environment variables. The daemon can be started by supplying the
command ``daemon`` to the ``slmon`` script. Let's look at an example:

* Use the Solar-Log™ at ``http://solar-log-1234/``
* Log in as ``user``, this is the default and is omitted for this reason.
* Enable dumping the result to the filesystem
* Tell it to dump to ``/tmp/solarlog``
* Enable debug mode to get verbose output to the terminal
  
To make reading easier, the following command is broken into multiple lines, which is a feature of most shells (such as
Bash). It is done solely for keeping the output below a certain width:

.. code-block:: shell-session

   $ SLMON_SOLARLOG_ADDRESS=solar-log-1234 \
   > SLMON_SOLARLOG_LOGIN_PASSWORD=xeegexiekeeroo6paX8daish2 \
   > SLMON_ENABLE_DUMP=True \
   > SLMON_DUMP_DIR=/tmp/solarlog \
   > slmon --debug daemon
   2020-08-27 23:07:56,209 - slmon.daemon - INFO - Not using systemd module
   2020-08-27 23:07:56,209 - slmon.daemon - INFO - Daemon initializing
   2020-08-27 23:07:56,210 - slmon.daemon - DEBUG - Prometheus: preparing
   2020-08-27 23:07:56,210 - slmon.daemon - DEBUG - Prometheus: prepared
   2020-08-27 23:07:56,210 - slmon.daemon - DEBUG - Dumper: preparing
   2020-08-27 23:07:56,210 - slmon.dumper - DEBUG - Initialized with dir /tmp/solarlog
   2020-08-27 23:07:56,210 - slmon.dumper - DEBUG - Fixed ts to 2020-08-27 21:07:56.210570
   2020-08-27 23:07:56,210 - slmon.daemon - DEBUG - Dumper: prepared
   2020-08-27 23:07:56,210 - slmon.daemon - DEBUG - SolarLogClient: preparing
   2020-08-27 23:07:56,210 - slmon.daemon - DEBUG - SolarLogClient: prepared
   2020-08-27 23:07:56,210 - slmon.daemon - INFO - Ready to start the main loop
   2020-08-27 23:07:56,210 - slmon.daemon - INFO - Starting main loop

.. the pwgen is strong in this one, don't worry

The software starts up and prints a log message for each step. After starting the main loop, it will query the
data logger approximately every 15 seconds.
