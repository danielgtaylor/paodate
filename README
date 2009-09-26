Pao Date Tools
==============
Utilities for making date and time handling in Python easy. This is mainly
accomplished with the new Date object which abstracts most of the 
differences between datetime, date, time, timedelta, and relativedelta,
allowing you to convert freely between all of them and providing useful
utility methods. Some examples:

    >>> Date(1234567890).datetime
    datetime.datetime(2009, 2, 14, 0, 31, 30)
    
    >>> d = Date(datetime(2004, 1, 12))
    >>> d.day += 10
    >>> d
    Date(2004-01-22, 00:00:00)
    
    >>> d.friendly
    '22 Jan 2004'
    
    >>> d.sql
    "'2004-01-22 00:00:00'"
    
    >>> d.month_tuple
    (Date(2004-01-01, 00:00:00), Date(2004-01-31, 23:59:59))

Please take a look at the well-documented paodate.py file for more
information.

Usage
-----
Import the paodate.py file into your project and use the Date object.

Requirements
------------
This module requires Python and the dateutil module. To run all tests
and make sure everything works for you installation please run this module
as a script, which will invoke the unit tests.

Authors & Contributors
----------------------
Daniel G. Taylor <dan@programmer-art.org>

License
-------
This module is free software, released under the terms of the Python 
Software Foundation License version 2, which can be found here:

    http://www.python.org/psf/license/


