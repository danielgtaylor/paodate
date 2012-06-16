from distutils.core import setup

setup(
    name = "paodate",
    version = "1.2",
    description = "Easy object-oriented date and time handling for Python",
    long_description = """Overview
========
Utilities for making date and time handling in Python easy. This is mainly
accomplished with the new Date object which abstracts most of the 
differences between datetime, date, time, timedelta, and relativedelta,
allowing you to convert freely between all of them and providing useful
utility methods.

Please look at the README.rst file included with this project and the
source code documentation and examples for more information.
""",
    author = "Daniel G. Taylor",
    author_email = "dan@programmer-art.org",
    url = "https://github.com/danielgtaylor/paodate",
    download_url = "https://github.com/danielgtaylor/paodate/zipball/master",
    py_modules = [
        "paodate",
    ],
    provides = [
        "paodate",
    ],
    keywords = "date time timespan sql",
    platforms = [
        "Platform Independent",
    ],
)
