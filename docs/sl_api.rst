
.. _sl-api:

#######
Web-API
#######

The API of the data logger revolves around two endpoints, one for querying data and one for changing data. The latter
is called ``/setjp`` and not used by SLMON, the query endpoint is ``/getjp`` and both operate on ``POST`` requests
only. There are some additional endpoints used for session handling, too.

.. warning::

   **Risk of data loss**

   When interacting with the Solar-Log™, use extreme caution or develop against a non-productive device. It is possible
   to crash the device by requesting too much data or using invalid queries. The device may enter a crash loop and lose
   all data and configuration if it happens. Always have backups ready.

If the device crashes (or returns too many HTTP 500 in short sequence), it may enter a locked down mode where it waits
for an operator to open its website and decide what to do. This is intended to be able to recover the device if
something went wrong instead of crashing endlessly if the stored data is invalid.

Query format quickstart
***********************
The query format works by sending a JSON structure to the ``/getjp`` endpoint and having it "fill in" the `null`
values. An example query for the "Open JSON" can be found in the manual. It sends the string ``{"801":{"170":null}}``
to the `getjp` endpoint, which then fills in the ``null`` in the data structure with values. The query works without
login and can be used to create the first useful dashboards.

.. code-block:: shell-session

   $ curl -X POST -H "Content-Type: application/json" -d '{"801":{"170":null}}' "http://<solar-log>/getjp" 2> /dev/null | jq .
   {
     "801": {
       "170": {
         "100": "27.08.20 21:22:15",
         "101": 0,
         "102": 0,
         "103": 0,
         "104": 77,
         "105": 27000,
         "106": 37000,
         "107": 779000,
         "108": 1689000,
         "109": 1689000,
         "110": 393,
         "111": 12953,
         "112": 14742,
         "113": 403653,
         "114": 423009,
         "115": 423009,
         "116": 7800
       }
     }
   }

As can be seen, the ``null`` value of the ``170`` key was filled with data, and that's basically how the entire API
works. All keys are basically integers, and the challenge is to find out what they correspond to. This format was
probably chosen to increase efficiency of the software, as it does not have to deal with string parsing. The data
logger is an embedded device, after all.

.. note::

   While tempting, there is no sense in simply querying for ``{"801":null}`` as most of the data is not available
   without login, and there are some queries that can crash the device and force it to reboot. More on that topic
   later.

User and Permission management
******************************
The devices support multiple user accounts, with the basic user being called `User` that can query most of the data.
Two other users are `Admin` and `Installer`. Their internal names are ``user``, ``admin`` and ``installer`` with the
level of access rising from `user` to `installer`. The website code suggests that there are at least two more levels.

Most of the time, this documentation will refer to users as levels:

* ``Level 0`` has no permissions other than querying the Open JSON explained above (plus very few extra fields) and is
  the basic level when no login session exists.
* ``Level 1`` refers to the normal ``user`` account that most endusers use. It can view most of the data and can enter
  the `Diagnostics` and `Configuration` sections of the web page. Almost all settings can be viewed but most can't be
  changed.
* ``Level 1`` corresponds to the ``admin`` user that can view more data fields than the previous level and can change
  most of the settings not relevant to managing grid feed.
* ``Level 2`` finally is the ``installer`` user that can view almost all data fields and can, in addition to all the
  above, manage grid feed settings.

In some tables, these levels are shortened to ``LVL0`` to ``LVL2`` in order to keep them narrower.

Querying the current level
==========================
There is an API endpoint available that can be queried from any level called `logcheck`. Simply ``GET`` the
``/logcheck`` endpoint like so:

.. code-block:: shell-session

   $ curl -X GET "http://<solar-log>/logcheck" 2> /dev/null
   0;0;0

This tripple is used to manage permission and access levels inside the javascript code of the website. The numbers
correspond to the levels above.

.. todo:: explain better

Logging in
==========
The ``/login`` endpoint handles the part of logging in as a user. Logging in is accomplished by sending the username
and password as form data ``u`` and ``p`` respectively.

On success, the response code ``200`` is returned and the body of the response will read ``SUCCESS - Password was
correct, you are now logged in`` with a newline at the end. The session token is sent as a cookie named ``SolarLog`` as
an ASCII string.


Logging out
===========
Manually terminating a session can be accomplished by sending an empty ``POST`` request to the ``/logout`` endpoint. If
no session exists or the cookie contains an invalid session a return code of ``200`` is returned along with the text
``FAILED - You were not logged in!``.

Session handling
****************
The device supports one single session. That means that while the Open JSON data can be queried at all time, any
further data can only be queried while no one is logged into the device. Opening a new session will automatically
terminate the existing one. To maintain a session across requests, obtain a cookie as shown in the `Logging in` section
and send cookie (named `SolarLog`) along each request.

Other endpoints
***************
* Licenses and software versions
* LCD
* ...

