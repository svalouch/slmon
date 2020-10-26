
###############
SLMON Overview
###############

The main purpose of SLMON is to continuously query a single Solar-Log™ data logger and expose the results via a number
of means. It's configuration is done using environment variables (see :ref:`mon_operation-configuration`).
Additionally, there are subcommands for reading dumped data (see below).

Solar-Log™ access
*****************
The SLMON daemon queries API endpoints on the devices website. It provides the same information as can be seen when
accessing the website with a regualar browser. At the minimum, it queries the ``Open JSON`` data (internally known as
`Open Data`) that is described in the manual. In addition to that, it is able to log into the Solar-Log™ and query more
information.

As the device supports a single session only, the daemon can be instructed to stop renewing its session when it ends by
sending a ``SIGUSR1`` and resume later using ``SIGUSR2``. See :ref:`mon_operation-session_handling` in the Operation
instructions for more info on that topic.

Data exposition
***************
The data queried from the Solar-Log™ device is exposes using a number of configurable writers. These can be enabled
when starting the daemon using environment variables (see :ref:`mon_operation-configuration`).

Available writers are:

* **InfluxDB**
* **Prometheus**
* **PostgreSQL** (experimental)

Additionally, a **Dumper** can be enabled that dumps everything that was received to the filesystem, e.g. as a backup
or for later analysis (see :ref:`mon_operation-configuration-dumper`).

InfluxDB
========
The InfluxDB writer connects to a server and uses a pre-existing database to write the data to. It requires the name of
the Solar-Log™ which it includes as tag ``sl`` in the measurements (tables). The configuration is detailed in
:ref:`mon_operation-configuration-influxdb`.

The following measurements are written:

* ``open_data`` contains the data from the `Open JSON` API noted in the manual.
* ``battery`` contains battery metrics (voltage, charge, charge/discharge power).

Prometheus
==========
Prometheus follows a pull-principle and thus the daemon exposes the metrics at a web api endpoint and waits for the
Prometheus server to scrape it. In addition to exposing the data received from the device, this is also where the
internal state of the application is exposed, so that Prometheus can be used to monitor the operation of SLMON. The
same endpoint is used for monitoring and exposition, the monitoring data is always exported if exposition is activated.

Note that other than both `InfluxDB` and `PostgreSQL`, this writer does not expose the name given in the config as it
is preferred to attach such metrics in the scrape configuration. See the following example for a scrape config that
queries two instances on two computers:

.. code-block:: yaml

   ---
   scrape_configs:
     - job_name: slmon
       static_configs:
         - targets:
             - 127.0.0.1:8081
           labels:
               location: backyard
               sl: sl1
         - targets:
             - 192.168.0.1:8081
           labels:
               location: frontyard
               sl: sl2

The configuration is described in :ref:`mon_operation-configuration-prometheus`.

PostgreSQL
==========

.. warning::

   The PostgreSQL writer is not working at the moment.

Although not the first thing that comes to mind when thinking about timeseries database, PostgreSQL performs really
well when used as one. As with InfluxDB, it requires the name of the Solar-Log™ device. Its configuration is detailed
in :ref:`mon_operation-configuration-postgresql`.

The following tables need to exist:

* ``event`` records the timestamps, and device name. All the other tables reference it.
* ``open_data`` contains the data from the `Open JSON` API noted in the manual.
* ``battery`` contains battery metrics
