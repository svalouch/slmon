
:wide_page: true

.. _sl-structure-overview:

##################
Structure Overview
##################

This is the main datastructure overview. It contains every discovered data structure, branching out to some particular
large structures where appropriate. These and the detail structures on extra pages focus (almost) exclusively on
querying data, not changing it. That means that all of the permissions and examples are for getting data out of the
device using the ``/getjp`` endpoint.

Note that some structures can return different results (such as subsets) when called differently. For example, a
request for ID ``32000`` in structure ``141`` returns inventory data instead of stored measurements. There's also a
``preval`` and ``postval`` parameter that is not covered (yet).

.. include:: _data_structures_legend.rst

Info marked ``(IOB)`` is taken from
`ioBroker.solarlog <https://github.com/iobroker-community-adapters/ioBroker.solarlog>`_.

Structures 100-199
******************

.. csv-table:: Structures 100-199
   :header-rows: 1
   :widths: 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 24, 35
   :file: table_r_100.csv

Structures 200-299
******************

.. csv-table:: Structures 200-299
   :header-rows: 1
   :widths: 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 24, 35
   :file: table_r_200.csv

Structures 300-399
******************

.. csv-table:: Structures 300-399
   :header-rows: 1
   :widths: 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 24, 35
   :file: table_r_300.csv

Structures 400-499
******************

.. csv-table:: Structures 400-499
   :header-rows: 1
   :widths: 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 24, 35
   :file: table_r_400.csv

Structures 500-599
******************

.. csv-table:: Structures 500-599
   :header-rows: 1
   :widths: 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 24, 35
   :file: table_r_500.csv

Structures 600-699
******************

.. csv-table:: Structures 600-699
   :header-rows: 1
   :widths: 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 24, 35
   :file: table_r_600.csv

Structures 700-799
******************

.. csv-table:: Structures 700-799
   :header-rows: 1
   :widths: 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 24, 35
   :file: table_r_700.csv

Structures 800-899
******************

.. csv-table:: Structures 800-899
   :header-rows: 1
   :widths: 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 24, 35
   :file: table_r_800.csv

Structures 900-999
******************

**Does not exist**

Structures 10000-10099
**********************

No structures exist for reading. However, when writing values using ``setjp``, then the key ``10000`` is set to ``0``.

.. 862 big
   863 big
   query = ``{"141":{"32000":{"145":null,"149":null,"158":null}},"145":{"100":{"0":{"100":null}}},"161":null,"170":null,"172":null,"199":{"100":null},"221":null,"223":null,"226":null,"266":null,"319":{"100":null},"328":null,"387":null,"412":null,"440":null,"489":null,"497":{"32000":{"101":null,"108":null}},"527":null,"613":null,"614":null,"615":null,"800":{"111":null,"151":null,"170":null,"174":null},"801":{"100":null,"125":null,"127":null},"871":{"100":null}}``

