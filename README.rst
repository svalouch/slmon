###############################################
SLMON - Data logger for Solar-Log™ data loggers
###############################################

The main purpose is to extract data from existing Solar-Log™ data loggers produced by `Solare Datensysteme GmbH` and
make it available for other services to consume, such as pushing it to an InfluxDB database.

This software, the documentation and other contents of the repository are not affiliated with or supported by Solare
Datensysteme GmbH, but are independently developed by volunteers. Solar-Log™ and WEB Enerest™ are trademarks of Solare
Datensysteme GmbH.

SLMON, the main software, interfaces with the data logger via its web interface. In its simplest mode of operation, it
continuously queries the Open JSON data endpoint described in the manual. On top of that, it is capable of logging into
the device and extract more data than what is available without login. There are some strings attached, unfortunately,
you can find out more at the `main documentation <https://slmon.rtfd.io/>`_. The documentation also contains
information about the Solar-Log™ devices themselves, such as documenting the datastructures used, which may come in
handy when developing own solutions, too.

The project is still in its very early stages of development and there is not much working right now.


