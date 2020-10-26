
:wide_page: true

.. _sl-structure-143:

###########################
Structure: 143 - Statistics
###########################

This structure contains statistics as displayed in one of the diagnostics sections of the device. The innermost number
denotes the days back. This means that a value of ``0`` will be the (incomplete) statistics for the current day (today
minus zero days), ``1`` means yesterday and so on. The structure includes the day back relative to today in position
``ID3`` (the ``$i``) in the table below. This has the implication that the date at which the data was dumped needs to
be known, if it is dumped to a file without recording the date e.g. in the filename, the information becomes useless.

.. include:: _data_structures_legend.rst

The data has a granularity of 5 minutes and includes a timestamp in the form ``HH:MM:SS``.

This data structure could very well be dependant on the type and number of solar inverters installed. The following
dataset is from a device that monitors an inverter with two strings of solar panels. There is an integer
``$n/100/$i/0/2`` that could be used to set the number of strings the inverter has.

Structure
*********

.. csv-table:: Structure 143
   :header-rows: 1
   :widths: 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 24, 35
   :file: table_s_143.csv

The structure does not contain anything but the above mentioned ``100`` and ``101`` structures.
