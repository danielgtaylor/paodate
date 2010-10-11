Pao Date Tools
==============
Utilities for making date and time handling in Python easy. This is mainly
accomplished with the new Date object which abstracts most of the 
differences between datetime, date, time, timedelta, and relativedelta,
allowing you to convert freely between all of them and providing useful
utility methods.

Please note that examples on this page assume a timezone of UTC+1 
(Europe/Amsterdam), as is set before running the unit tests so that all times 
are in a common timezone, otherwise the tests would all be off by some number 
of hours depending on your local timezone.

Some quick examples:

    >>> from paodate import Date
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

Constructors
------------
Date objects can be created from just about anything you might want, including 
Python datetime and date objects, struct_time objects, numbers, lists, tuples, 
and strings (which require an extra format parameter):

    >>> Date()
    # This will be right now in local time on your system
    
    >>> Date(1234567890)
    Date(2009-02-14 00:31:30)
    
    >>> Date(datetime(2009, 2, 14, 0, 31, 30))
    Date(2009-02-14 00:31:30)
    
    >>> Date(date(2009, 2, 14))
    Date(2009-02-14 00:00:00)
    
    >>> Date(time.localtime(1234567890))
    Date(2009-02-14 00:31:30)
    
    >>> Date((2009, 2, 14, 0, 31, 30))
    Date(2009-02-14, 00:31:30)
    
    >>> Date("2009.02.14 at 00:31:30", format="%Y.%m.%d at %H:%M:%S")
    Date(2009-02-14, 00:31:30)

You can also construct a Date object in the past (or future) by passing in the
modification type and amount:

    >>> d = Date(months_ago=3)
    # This will be three months ago from today in local time
    
    >>> d = Date(years_ago=1, months_ago=2, days_ago=-5)
    # One year and two months ago from five days in the future from today

Conversion
----------
Converting a Date object to any representation you might need is incredibly simple:

    >>> d = Date(1234567890)
    
    >>> d.datetime
    datetime.datetime(2009, 2, 14, 0, 31, 30)
    
    >>> d.date
    datetime.date(2009, 2, 14)
    
    >>> d.time
    datetime.time(0, 31, 30)
    
    >>> d.tuple
    time.struct_time(tm_year=2009, tm_mon=2, tm_mday=14, tm_hour=0, tm_min=31,
                     tm_sec=30, tm_wday=5, tm_yday=45, tm_isdst=-1)
    
    >>> d.timestamp
    1234567890

It is also possible to convert an existing Date object to UTC (this essentially
removes time zone information after adjusting by the local offset):

    >>> d.utc
    Date(2009-02-13, 23:31:30)

Component Access
----------------
All date and time components of the Date object may be read and written to.
When writing to the components it is good practice to never use absolute values
and instead use the += and -= operators, as setting negative component values
can have unintended effects.

    >>> d = Date(1234567890)
    >>> d
    Date(2009-02-14, 00:31:30)
    
    >>> d.day += 5
    >>> d
    Date(2009-02-19, 00:31:30)
    
    >>> print d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond
    2009, 2, 19, 0, 31, 30, 0
    
    >>> d.year -= 3
    >>> d
    Date(2006-02-19, 00:31:30)

It's also possible to quickly add / subtract all the components except 
microseconds at once or to daisy-chain such operations:

    >>> d.add(years=-2, days=13, minutes=5)
    # Subtract two years, add 13 days and 5 minutes
    
    >>> d = Date().start_of_month.add(days=-3)
    # Get the date and time three days before the start of the current month

The number of days in the current month is also built-in:

    >>> d.days_in_month
    28

Getting whether this date is in the past or future is easy as well:

    >>> d.is_past_date
    True
    >>> d.is_today
    False
    >>> d.is_future_date
    False

Addition and subtraction of Date objects is also somewhat possible. Addition 
is possible between a Date and datetime.timedelta, and subtraction is possible 
between Date objects and a Date and a datetime.timedelta:

    >>> d = Date(1234567890)
    >>> d2 = Date(1234567900)
    >>> delta = d2 - d
    >>> delta
    datetime.timedelta(0, 10)
    >>> d + delta
    Date(2009-02-14, 00:31:40)

Relevant Adjacent Dates and Ranges
----------------------------------
Many times in an application you need to get the current month, or the current
day for queries such as all posts from today, the amount to charge a customer
for this month, etc. The Date object has all these useful ranges built-in, and
they all return new Date objects which you can then convert as you see fit.

    >>> d = Date(1234567890)
    >>> d
    Date(2009-02-14, 00:31:30)
    
    >>> d.start_of_day
    Date(2009-02-14, 00:00:00)
    >>> d.end_of_day
    Date(2009-02-14, 23:59:59)
    >>> d.day_tuple
    (Date(2009-02-14, 00:00:00), Date(2009-02-14, 23:59:59))
    >>> [x.timestamp for x in d.day_tuple]
    [1234501200, 1234587599]
    
    >>> d.week_tuple
    (Date(2009-02-09, 00:00:00), Date(2009-02-15, 23:59:59))
    
    >>> d.start_of_month
    Date(2009-02-01, 00:00:00)
    >>> d.month_tuple
    (Date(2009-02-01, 00:00:00), Date(2009-02-28, 23:59:59))
    
    >>> d.end_of_year
    Date(2009-12-31, 23:59:59)
    >>> d.year_tuple
    (Date(2009-01-01, 00:00:00), Date(2009-12-31, 23:59:59))

Representation
--------------
The following useful representations are built into the Date object:

    >>> d = Date(1234567890)
    >>> d.friendly
    '14 Feb 2009'
    
    >>> d.fancy
    'February 14th, 2009'
    >>> d.fancy_no_year
    'February 14th'
    
    >>> d.sql
    '2009-02-14 00:31:30'
    >>> d.sql_date
    '2009-02-14'
    >>> d.sql_time
    '00:31:30'
    
    >>> d.strftime("%Y-%m-%d")
    '2009-02-14'

Please take a look at the well-documented paodate.py file for more
information.

Usage
-----
Import the paodate.py file into your project and use the Date object.

Requirements
------------
The only requirement for this module is Python. Running this script will
invoke all unit tests so you can see that everything works for your
installation.

Authors & Contributors
----------------------
Patches are very welcome upstream, so feel free to fork and push your changes
back up! The following people have worked on this project:

    * Daniel G. Taylor <dan@programmer-art.org>

License
-------
This module is free software, released under the terms of the Python 
Software Foundation License version 2, which can be found here:

    http://www.python.org/psf/license/


