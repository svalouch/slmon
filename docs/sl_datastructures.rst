
.. _sl-datastructures:

##############
Datastructures
##############

This section deals with the datastructures used by the dataloggers. The same structures appear in almost every part of
of the devices, such as:

* They drive the website presented by the device for monitoring, configuration and so on. The single-page-applications
  javascript code decodes the data on the fly.
* Data and configuration backup and restore
* Data transfer to WEB-Enerest™

Head over to the :ref:`sl-api` page for more information about how to interact with the API endpoints ``/getjp`` and
``/setjp``.

.. note::

   The focus of this project is data extraction and the `setjp` endpoint is largely ignored.

This project is focusing on getting data out of the device and ignores the `setjp` endpoint. The structures are indexed
from ``100`` up to the ``900``\s. The main overview page of the data structures contains the entire index as far as it
has been discovered, branching out to individual subpages for large data structures.

.. toctree::
   :maxdepth: 1
   :caption: Data structures

   sl_structures_overview
   sl_structure_141
   sl_structure_143
   sl_structure_800
   sl_structure_801
   sl_structure_860
