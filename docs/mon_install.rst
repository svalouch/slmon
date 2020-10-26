
#########################
Installation instructions
#########################

At this stage, there are no packages for SLMON. Thus, the recommended way is to either install it into a virtualenv or
to create a virtualenv within a clone of the repository and perform an "editable" installation.

Requirements
************
SLMON is written in Python 3 and requires a few extra Python modules. The software is primarily written to support
Python versions ``3.7`` and up. It should therefor work on most modern Linux distributions, e.g. ones that are based on
Debian Buster (Raspbian) or Ubuntu 20.04, Arch and Gentoo.

Required packages:

* ``click`` is used to implement the commands.
* ``requests`` for querying the datalogger.
* ``influxdb`` implements the InfluxDB connection.
* ``prometheus_client`` version ``0.7`` and above, used to provide the application monitoring and optionally export the
  measurements, too.
* ``pydantic`` used for settings and data handling.
* ``psycopg2`` for the experimental PostgreSQL support, this will most likely be made optional in the future.

Virtualenv / Pip
****************

With this approach, the software will be installed into a virtual Python environment and can be used by accessing the
generated entry points. This is primarly intended to just use the software.

There are a number of virtualenv implementations that all work more or less the same for the intended purpose. The
authors commonly use the Python `venv` module, which is usually available in a package called ``python3-venv`` or
similar, depending on your distribution.

The sequence of operation is:

#. Create the empty virtualenv
#. Activate it
#. Install the software

.. code-block:: shell-session

   $ python3 -m venv venv
   $ source venv/bin/activate
   (venv) $ pip install "git+https://github.com/svalouch/slmon.git#egg=slmon"
   Collecting sl_mon
   [...]
   Successfully installed [...] sl_mon
   $ slmon --help
   Usage: slmon [OPTIONS] COMMAND [ARGS]...

   Options:
   [...]

It is possible to run the software without first activating the virtualenv by calling it with the absolute path, e.g.
to integrate it into a process manager such as OpenRC or SystemD:

``path/to/venv/bin/slmon --help``

Editable Virtualenv (for development)
*************************************

This approach clones the repository first, then changes into it and creates the virtualenv inside the directory. The
software is then installed in an "editable" way, which means that the sources can be edited and the changes applied
immediately without having to reinstall it each time a change was made. This is primarily indended for development.

The sequence of operation is almost identical to the above way:

#. Clone the repository
#. Enter the new directory and create a virtualenv
#. Install the software "editable"

.. code-block:: shell-session

   $ git clone https://github.com/svalouch/slmon.git
   Cloning into `slmon`...
   remote: Enumerating objects: 219, done.
   [...]
   $ cd slmon
   $ python3 -m venv venv
   $ source venv/bin/activate
   (venv) $ pip install -e .
   Obtaining [...]
   [...]
   Successfully installed slmon
   $ slmon --help
   Usage: slmon [OPTIONS] COMMAND [ARGS]...

   Options:
   [...]

As before, the script is in the ``venv/bin`` directory and can be called without activating the virtualenv by
specifying the full path. All changes made to the code are immediately available when the software is started.

