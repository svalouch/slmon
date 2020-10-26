
#########
Inventory
#########

The Solar-Log™ maintains an inventory of connected devices, which are usually identified by their ID (device ID or
``DID``).

Serial numbers (740)
********************
Although serial numbers are maintained for many devices, the field often contains the device address or a combination
of device address and serial number. The serial number is in structure ``740``, which mapps it to the device ID. A
device that exposes multiple addresses, such as RCT inverters (inverter + energy meter) appear multiple times with the
same serial number but a different address.

* ``1 / 123123`` means that a device with the serial number ``123123`` uses address ``1``. In this case, it is an
  energy meter connected via ModbusRTU.
* ``2 / 123123`` is the same (physical) device as above, but using a different address (2 instead of 1).
* ``192.168.0.1`` is the IP address of a device connected via Ethernet. This is used, e.g. for intelligent consumers
  such as heat pumps.

Vendors (744)
*************
Vendors are maintained as IDs, and structure ``744`` mapps vendor names to IDs.

Query: ``{"744":null}``.

Device stanzas (739)
********************
Device stanzas contain settings for how to use a device and what kind of device it is. They are maintained in the
structure ``739``. Each stanza is an array of elements that may or may not contain information. Of interest may be:

* ``0`` is the vendor ID for use with structure ``744``
* ``3`` is the RS485 or RS455 baud rate to use
* ``5`` is a bit field, which allows the device to represent multiple classes such as "Inverter and Energy meter".
* ``6`` is the device ID

Configured devices (141)
************************
Configured devices are maintained in the ``141`` structure, which poses a problem as this structure can't be queried
reliably without risking a crash of the web application, potentially causing the Solar-Log™ to lock itself down because
of frequent errors, requiring human intervention.

Luckily, the special device ID ``32000`` can be used to retrieve the definitions rather than measurement data, and the
fields ``119`` then contain the user-supplied device name (such as `Inverter 1`) and ``162`` linking it to the stanza
(see above).

As such, to build an inventory, use the following query: ``{"141:{"32000":{"119":null,"162":null}}}``.
