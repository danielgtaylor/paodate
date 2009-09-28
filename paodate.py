#!/usr/bin/env python
 
"""
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

"""
 
import calendar
import time
 
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
 
class Date(object):
    """
        An object representing a date and a time. This object has several
        advantages over Python's built-in date and time objects.
        
         * Attributes like the year, month, hour, etc are writable
         * You can easily get the datetime, date, tuple, and timestamp.
           representation of this date.
         * Convenience methods for various string representations.
         * Convenience methods for (start, end) tuples of the current day,
           month, or year.
        
            >>> d = Date(123456)
            >>> str(d)
            'Date(1970-01-02, 11:17:36)'
            >>> d.year += 10
            >>> str(d)
            'Date(1980-01-02, 11:17:36)'
            >>> d.month = 6
            >>> str(d)
            'Date(1980-06-02, 11:17:36)'
            >>> d.day += 256
            >>> str(d)
            'Date(1981-02-13, 11:17:36)'
            >>> d.day, d.month, d.year
            (13, 2, 1981)
            >>> d.tuple                     # doctest: +NORMALIZE_WHITESPACE
            time.struct_time(tm_year=1981, tm_mon=2, tm_mday=13, tm_hour=11,
                             tm_min=17, tm_sec=36, tm_wday=4, tm_yday=44,
                             tm_isdst=-1)
            >>> d.timestamp
            350907456
            >>> d.date
            datetime.date(1981, 2, 13)
            >>> d.datetime
            datetime.datetime(1981, 2, 13, 11, 17, 36)
            >>> d > Date(12345)
            True
            >>> d < Date(12345)
            False
        
    """
    def __init__(self, dt = None, years_ago = 0, months_ago = 0, days_ago = 0,
                 hours_ago = 0, minutes_ago = 0, seconds_ago = 0):
        """
            Create a new Date object, optionally passing in a timestamp, date or 
            datetime object to set the date/time from. If it is not given then 
            the date/time are set to now.
            
                >>> Date(1234567890)
                Date(2009-02-14, 00:31:30)
                >>> Date((2009, 2, 14))
                Date(2009-02-14, 00:00:00)
                >>> Date(date(2009, 10, 2))
                Date(2009-10-02, 00:00:00)
                >>> Date(datetime(2007, 3, 24))
                Date(2007-03-24, 00:00:00)
            
            @type dt: timestamp, tuple, date, or datetime
            @param dt: Date/time to set; if None the current date/time will
                       be set.
            @type years_ago: int
            @param years_ago: The number of years ago from dt to set the date
            @type months_ago: int
            @param months_ago: The number of months ago from dt to set the date
            @type days_ago: int
            @param days_ago: The number of days ago from dt to set the date
            @type hours_ago: int
            @param hours_ago: The number of hours ago from dt to set the date
            @type minutes_ago: int
            @param minutes_ago: The number of minutes ago from dt to set the
                                date
            @type seconds_ago: int
            @param seconds_ago: The number of seconds ago from dt to set the
                                date
            @raise ValueError: If dt is not an int, date, or datetime object
        """
        if dt is None:
            self.dt = datetime.now()
        elif type(dt) in [float, int, long]:
            self.dt = datetime.fromtimestamp(dt)
        elif type(dt) in [list, tuple]:
            self.dt = datetime(*dt)
        elif type(dt) is date:
            self.dt = datetime.combine(dt, datetime.min.time())
        elif type(dt) is datetime:
            self.dt = dt
        else:
            raise ValueError("You must pass an int, long, float, 9-item " \
                             "list or tuple, date or datetime object! Got " \
                             "%s instead!" % str(dt))
        
        for time_ago in ["years_ago", "months_ago", "days_ago", "hours_ago",
                         "minutes_ago", "seconds_ago"]:
            exec("self.%s -= %s" % (time_ago.split("_")[0][:-1], time_ago))
 
    def __repr__(self):
        """
            Return a nice string representation of this date.
            
                >>> str(Date(datetime(2009, 10, 2)))
                'Date(2009-10-02, 00:00:00)'
            
        """
        return self.strftime("Date(%Y-%m-%d, %H:%M:%S)")
    
    def __add__(self, value):
        """
            Pass additions in to the datetime object so that timedeltas still
            work!
            
                >>> d = Date(1234567890)
                >>> d + timedelta(days = 2)
                Date(2009-02-16, 00:31:30)
            
            @rtype: Date
            @return: The modified date object
        """
        return Date(self.dt.__add__(value))
    
    def __cmp__(self, value):
        """
            Compare this date object to another date object.
            
                >>> Date(12345) > Date(1234)
                True
                >>> Date(12345) < Date(1234)
                False
                >>> Date(12345) == Date(12345)
                True
            
            @rtype: int
            @return: -1 if it is smaller, 0 if they are equal, 1 if it is
                     greater than the other date object
        """
        if type(value) == Date:
            return cmp(self.dt, value.dt)
        else:
            raise TypeError("Invalid type!")
    
    def _get_datetime(self):
        """
            Return a datetime representation of this date/time, as would be
            given by datetime(...)
            
                >>> Date(1234567890).datetime
                datetime.datetime(2009, 2, 14, 0, 31, 30)
            
            @rtype: datetime
            @return: The datetime representation of this date/timme
        """
        return self.dt
    
    def _set_datetime(self, value):
        """
            Set the time from a datetime object.
            
                >>> d = Date(1234567890)
                >>> d.datetime = datetime(2009, 02, 14)
                >>> d
                Date(2009-02-14, 00:00:00)
            
            @type value: datetime
            @param value: The date/time to set
        """
        self.dt = value
    
    datetime = property(_get_datetime, _set_datetime)
    
    def _get_date(self):
        """
            Return a date representation of this date/time, as would be
            given by date(...)
            
                >>> Date(1234567890).date
                datetime.date(2009, 2, 14)
            
            @rtype: date
            @return: The date representation of this date/timme
        """
        return self.dt.date()
    
    def _set_date(self, value):
        """
            Set the date from a date object.
            
                >>> d = Date(1234567890)
                >>> d.date = date(2009, 2, 14)
                >>> d
                Date(2009-02-14, 00:31:30)
            
            @type value: date
            @param value: The date to set
        """
        self.dt = datetime.combine(value, self.dt.time())
    
    date = property(_get_date, _set_date)
    
    def _get_time(self):
        """
            Return a time representation of this date/time, as would be
            given by time(...)
            
                >>> Date(1234567890).time
                datetime.time(0, 31, 30)
            
            @rtype: time
            @return: The time representation of this date/timme
        """
        return self.dt.time()
    
    def _set_time(self, value):
        """
            Set the time from a time object.
            
                >>> d = Date(1234567890)
                >>> d.time = datetime(1980, 5, 23, 11, 2, 45).time()
                >>> d
                Date(2009-02-14, 11:02:45)
            
            @type value: time
            @param value: The time to set
        """
        self.dt = datetime.combine(self.dt.date(), value)
    
    time = property(_get_time, _set_time)
    
    def _get_tuple(self):
        """
            Return a tuple representation of this time, as would be given
            by datetime.timetuple()
            
                >>> Date(1234567890).tuple  # doctest: +NORMALIZE_WHITESPACE
                time.struct_time(tm_year=2009, tm_mon=2, tm_mday=14, 
                                 tm_hour=0, tm_min=31, tm_sec=30, tm_wday=5, 
                                 tm_yday=45, tm_isdst=-1)
            
            @rtype: tuple
            @return: (year, month, day, hour, minute, second, weekday, 
                      year day, is daylight saving)
        """
        return self.dt.timetuple()
    
    def _set_tuple(self, value):
        """
            Set the time from a tuple as would be given by datetime.timetuple()
            
                >>> d = Date()
                >>> d.tuple = (2009, 2, 14, 0, 31, 30, 0, 0, -1)
                >>> d
                Date(2009-02-14, 00:31:30)
            
            @type value: time.struct_time or tuple
            @param value: (year, month, day, hour, minute, second, microsecond,
                           ?, tz)
        """
        self.dt = self.dt.fromtimestamp(int(time.mktime(value)))
    
    tuple = property(_get_tuple, _set_tuple)
    
    def _get_timestamp(self):
        """
            Get this date represented as a Unix timestamp. If this date is
            beyond MAX defined above, then MAX_TS is returned to prevent
            ValueError exceptions when converting to a timestamp.
            
                >>> Date(1234567890).timestamp
                1234567890
            
            Note: You cannot represent all possible dates with a timestamp
            value, and if you attempt to you may get an exception!
            
            @rtype: int
            @return: The timestamp representation of this date
        """
        if self > MAX:
            return MAX.timestamp
        else:
            return int(time.mktime(self.dt.timetuple()))
    
    def _set_timestamp(self, value):
        """
            Set this date from a Unix timestamp.
            
                >>> d = Date()
                >>> d.timestamp = 1234567890
                >>> d
                Date(2009-02-14, 00:31:30)
            
            @type value: int
            @param value: The timestamp to set
        """
        self.dt = self.dt.fromtimestamp(value)
    
    timestamp = property(_get_timestamp, _set_timestamp)
 
    def _get_year(self):
        """
            Get this date's year.
            
                >>> Date(1234567890).year
                2009
            
            @rtype: int
            @return: The currently set year [0, 9999]
        """
        return self.dt.year
    
    def _set_year(self, value):
        """
            Set this dates year.
            
                >>> d = Date(1234567890)
                >>> d.year = 1984
                >>> d
                Date(1984-02-14, 00:31:30)
                >>> d.year += 6
                >>> d
                Date(1990-02-14, 00:31:30)
            
            @type value: int
            @param value: The year to set
        """
        self.dt = self.dt.replace(year = value)
    
    year = property(_get_year, _set_year)
    
    def _get_month(self):
        """
            Get this date's month.
            
                >>> Date(1234567890).month
                2
            
            @rtype: int
            @return: The currently set month [1, 12]
        """
        return self.dt.month
    
    def _set_month(self, value):
        """
            Set this date's month. If passed a value larger than 12 then the
            year will roll over.
            
                >>> d = Date(1234567890)
                >>> d.month = 6
                >>> d
                Date(2009-06-14, 00:31:30)
                >>> d.month -= 3
                >>> d
                Date(2009-03-14, 00:31:30)
            
            @type value: int
            @param value: The month to set
        """
        self.dt += relativedelta(months = value - self.dt.month)
    
    month = property(_get_month, _set_month)
    
    def _get_week(self):
        """
            Get this date's week of the year.
            
                >>> Date(1234567890).week
                6
            
            @rtype: int
            @return: The currently set week [1, 52]
        """
        delta = self.dt - datetime(self.dt.year, 1, 1)
        return delta.days / 7
    
    def _set_week(self, value):
        """
            Set this date to the given week of the current year. If the current
            day is e.g. a Tuesday then after this operation it will still be
            a Tuesday. If passed a value larger than 52 then the year will roll
            over.
            
                >>> d = Date(1234567890)
                >>> d.week = 12
                >>> d
                Date(2009-03-28, 00:31:30)
            
            @type value: int
            @param value: The week to set
        """
        week = self._get_week()
        self.dt += timedelta(weeks = value - week)
    
    week = property(_get_week, _set_week)
    
    def _get_day(self):
        """
            Get this date's day.
            
                >>> Date(1234567890).day
                14
            
            @rtype: int
            @return: The currently set day
        """
        return self.dt.day
    
    def _set_day(self, value):
        """
            Set this date's day. To set the day to the last day of the month
            please use either Date.end_of_month or Date.days_in_month, as
            setting it to a value larger than the number of days in the current
            month will cause the month to roll over!
            
                >>> d = Date(1234567890)
                >>> d.day = 1
                >>> d
                Date(2009-02-01, 00:31:30)
            
            @type value: int
            @param int: The day to set
        """
        self.dt += timedelta(days = value - self.dt.day)
    
    day = property(_get_day, _set_day)
    
    def _get_hour(self):
        """
            Get this date's hour.
            
                >>> Date(1234567890).hour
                0
            
            @rtype: int
            @return: The currently set hour
        """
        return self.dt.hour
    
    def _set_hour(self, value):
        """
            Set this date's hour. If set to a value larger than 24 it will
            cause the day to roll over.
            
                >>> d = Date(1234567890)
                >>> d.hour = 10
                >>> d
                Date(2009-02-14, 10:31:30)
            
            @type value: int
            @param value: The hour to set
        """
        self.dt += timedelta(hours = value - self.dt.hour)
    
    hour = property(_get_hour, _set_hour)
    
    def _get_minute(self):
        """
            Get this date's minute.
            
                >>> Date(1234567890).minute
                31
            
            @rtype: int
            @return: The currently set minute
        """
        return self.dt.minute
    
    def _set_minute(self, value):
        """
            Set this date's minute. If set larger than 60 it will cause the 
            hour to roll over.
            
                >>> d = Date(1234567890)
                >>> d.minute = 5
                >>> d
                Date(2009-02-14, 00:05:30)
            
            @type value: int
            @param value: The minute to set
        """
        self.dt += timedelta(minutes = value - self.dt.minute)
    
    minute = property(_get_minute, _set_minute)
    
    def _get_second(self):
        """
            Get this date's second.
            
                >>> Date(1234567890).second
                30
            
            @rtype: int
            @return: The currently set second
        """
        return self.dt.second
    
    def _set_second(self, value):
        """
            Set this date's second. If set larger than 60 it will cause the
            minute to roll over.
            
                >>> d = Date(1234567890)
                >>> d.second = 5
                >>> d
                Date(2009-02-14, 00:31:05)
            
            @type value: int
            @param value: The second to set
        """
        self.dt += timedelta(seconds = value - self.dt.second)
    
    second = property(_get_second, _set_second)
    
    def _get_microsecond(self):
        """
            Get this date's microsecond.
            
                >>> Date(1234567890).microsecond
                0
            
            @rtype: int
            @return: The currently set microsecond
        """
        return self.dt.microsecond
    
    def _set_microsecond(self, value):
        """
            Set this date's microsecond.
            
                >>> d = Date(1234567890)
                >>> d.microsecond = 250
            
            @type value: int
            @param value: The microsecond to set
        """
        self.dt += timedelta(microseconds = value - self.dt.microsecond)
    
    microsecond = property(_get_microsecond, _set_microsecond)
    
    @property
    def days_in_month(self):
        """
            Get the number of days in the currently set date's month.
            
                >>> Date(1234567890).days_in_month
                28
                >>> Date(472812932).days_in_month
                31
            
            @rtype: int
            @return: The number of days in the month
        """
        return calendar.monthrange(self.year, self.month)[1]
    
    def strftime(self, format = "%d %b %Y"):
        """
            Convert this date to a string. See time.strftime(...).
            
                >>> Date(1234567890).strftime("%Y-%m-%d, %H:%M:%S")
                '2009-02-14, 00:31:30'
            
            @type format: str
            @param format: The format string, see time.strftime(...)
            @rtype: str
            @return: The string representation of this date from format
        """
        return time.strftime(format, self.tuple)
    
    @property
    def start_of_day(self):
        """
            Get a new date with the time part of this date/time set to zero,
            i.e. 00:00:00.000000.
            
                >>> Date(1234567890).start_of_day
                Date(2009-02-14, 00:00:00)
            
            @rtype: Date
            @return: A new date with min time
        """
        tuple = self.dt.timetuple()
        return Date(datetime(tuple[0], tuple[1], tuple[2]))
    
    @property
    def end_of_day(self):
        """
            Get a new date with the time part of this date/time set to the max,
            i.e. 23:59:59.999999.
            
                >>> Date(1234567890).end_of_day
                Date(2009-02-14, 23:59:59)
            
            @rtype: Date
            @return: A new date with max time
        """
        tuple = self.dt.timetuple()
        return Date(datetime(tuple[0], tuple[1], tuple[2], 23, 59, 59, 999999))
    
    @property
    def start_of_month(self):
        """
            Get the start date/time of this month.
            
                >>> Date(1234567890).start_of_month
                Date(2009-02-01, 00:00:00)
            
            @rtype: Date
            @return: A new date set to the beginning of this month
        """
        return Date(datetime(self.dt.year, self.dt.month, 1))
    
    @property
    def end_of_month(self):
        """
            Get the end date/time of this month.
            
                >>> Date(1234567890).end_of_month
                Date(2009-02-28, 23:59:59)
            
            @rtype: Date
            @return: A new date set to the end of this month
        """
        return Date(datetime(self.dt.year, self.dt.month, 1, 23, 59, 59, 
                    999999) + relativedelta(months = 1, days = -1))
    
    @property
    def start_of_year(self):
        """
            Get the start date/time of this year.
            
                >>> Date(1234567890).start_of_year
                Date(2009-01-01, 00:00:00)
            
            @rtype: Date
            @return: A new date set to the beginning of this year
        """
        return Date(datetime(self.dt.year, 1, 1))
    
    @property
    def end_of_year(self):
        """
            Get the end date/time of this year.
            
                >>> Date(1234567890).end_of_year
                Date(2009-12-31, 23:59:59)
            
            @rtype: Date
            @return: A new date set to the end of this year
        """
        return Date(datetime(self.dt.year, 1, 1, 23, 59, 59, 999999) + \
                             relativedelta(years = 1, days = -1))
    
    @property
    def day_tuple(self):
        """
            Get a tuple of two L{Date}s representing the start and end of this
            day.
            
                >>> Date(1234567890).day_tuple
                (Date(2009-02-14, 00:00:00), Date(2009-02-14, 23:59:59))
                >>> tuple([d.timestamp for d in Date(1234567890).day_tuple])
                (1234566000, 1234652399)
            
            @rtype: tuple
            @return: (start, end) dates of the current day
        """
        return (self.start_of_day, self.end_of_day)
    
    @property
    def month_tuple(self):
        """
            Get a tuple of two L{Date}s representing the start and end of this
            month.
            
                >>> Date(1234567890).month_tuple
                (Date(2009-02-01, 00:00:00), Date(2009-02-28, 23:59:59))
                >>> tuple([d.date for d in Date(1234567890).month_tuple])
                (datetime.date(2009, 2, 1), datetime.date(2009, 2, 28))
            
            @rtype: tuple
            @return: (start, end) dates of the current month
        """
        return (self.start_of_month, self.end_of_month)
    
    @property
    def year_tuple(self):
        """
            Get a tuple of two L{Date}s representing the start and end of this
            year.
            
                >>> Date(1234567890).year_tuple
                (Date(2009-01-01, 00:00:00), Date(2009-12-31, 23:59:59))
            
            @rtype: tuple
            @return: (start, end) dates of the current year
        """
        return (self.start_of_year, self.end_of_year)
    
    @property
    def friendly(self):
        """
            Get a friendly representation of this date.
            
                >>> Date(datetime(2009, 2, 15)).friendly
                '15 Feb 2009'
            
            @rtype: str
            @return: The friendly representation of this date
        """
        return self.strftime("%d %b %Y")
    
    def _get_fancy(self, display_year = True):
        """
            Get a fancy representation of this date for invoices, forms, etc.
            
                >>> Date(datetime(2009, 2, 15)).fancy
                'February 15th, 2009'
            
            @rtype: str
            @return: The fancy representation of this date
        """
        if self.dt.day in [1, 21, 31]:
            extra = "st"
        elif self.dt.day == 2:
            extra = "nd"
        elif self.dt.day == 3:
            extra = "rd"
        else:
            extra = "th"
        
        if display_year:
            extra += ", %Y"
        
        return self.strftime("%B %d" + extra)
    
    fancy = property(_get_fancy)
    
    @property
    def fancy_no_year(self):
        """
            Get a fancy representation of this date for invoices, forms, etc.
            This version does not include the year!
            
                >>> Date(datetime(2009, 2, 15)).fancy_no_year
                'February 15th'
            
            @rtype: str
            @return: The fancy representation of this date minus the year
        """
        return self._get_fancy(False)
    
    @property
    def sql_date(self):
        """
            Return just the date portion of the SQL-friendly representation
            of this date/time.
            
                >>> Date(1234567890).sql_date
                "'2009-02-14'"
            
            @rtype: str
            @return: SQL-friendly representation of this date
        """
        return self.strftime("'%Y-%m-%d'")
    
    @property
    def sql_time(self):
        """
            Return just the time portion of the SQL-friendly representation
            of this date/time.
            
                >>> Date(1234567890).sql_time
                "'00:31:30'"
            
            @rtype: str
            @return: SQL-friendly representation of this time
        """
        return self.strftime("'%H:%M:%S'")
    
    @property
    def sql(self):
        """
            Get an SQL-friendly representation of this date/time that can be
            used in SQL expressions to be passed to a backend database.
            
                >>> Date(1234567890).sql
                "'2009-02-14 00:31:30'"
            
            @rtype: str
            @return: SQL-friendly representation of this date/time
        """
        return self.sql_date[:-1] + " " + self.sql_time[1:]
    
    @property
    def is_today(self):
        """
            Return whether this date is today or not.
            
                >>> Date(1234567890).is_today
                False
                >>> Date().is_today
                True
            
            @rtype: bool
            @return: True if this date is today, False otherwise
        """
        return self.dt.date() == datetime.today().date()
    
    @property
    def is_future_date(self):
        """
            Return whether this date (ignoring time) is in the future.
            
                >>> Date().is_future_date
                False
                >>> Date(days_ago = -1).is_future_date
                True
            
            @rtype: bool
            @return: True if this date is in the future, False otherwise
        """
        return self.dt.date() > datetime.today().date()
    
    @property
    def is_past_date(self):
        """
            Return whether this date (ignoring time) is in the past.
            
                >>> Date().is_past_date
                False
                >>> Date(12345).is_past_date
                True
            
            @rtype: bool
            @return: True if this date is in the past, False otherwise
        """
        return self.dt.date() < datetime.today().date()

"""
    The mininum and maximun dates are system-dependent, so we pick some 
    fairly sane defaults below that should be useful for most real-world
    applications. If they are not you can easily override them to suit
    your application domain.
"""
MIN = Date(0)
MAX = Date(datetime(2038, 1, 1))

if __name__ == "__main__":
    # Run unit tests for this module, e.g. via `python date.py` in a shell.
    import doctest
    doctest.testmod()

