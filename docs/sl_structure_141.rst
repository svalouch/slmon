
:wide_page: true

.. _sl-structure-141:

##############
Structure: 141
##############

.. include:: _data_structures_legend.rst

The data has a granularity of 5 minutes and includes a timestamp in the form ``HH:MM:SS``.

.. warning::

   This structure is immensely large and could result in the device returning HTTP 503 and finally enter a crash-loop
   where it must be reinitialized manually. Do **not** call the entire structure.

.. note::

   It looks like the structure components can be called by setting ``$i`` to ``32000``, such as
   ``{"141":{"32000":{"145":null,"149":null,"158":null}}}``.

Structure
*********

.. csv-table:: Structure 141
   :header-rows: 1
   :widths: 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 24, 35
   :file: table_s_141.csv

