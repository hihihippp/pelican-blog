Six Nations
##############

:date: 2010-10-03 10:20
:modified: 2010-10-04 18:40
:tags: thats, awesome
:category: yeah
:slug: my-super-post
:authors: Alexis Metaireau, Conan Doyle
:summary: Short version for index and feeds

As a European living in the States, time conversions are a little tricky
sometimes. I mean, yes, they basically boil down to basic addition and
subtraction, but it gets a little more complicated with several
timezones. As a keen rugby fan, I find myself calculating time
differences and looking up time zones more often than I would like. One
Friday night, I was bored enough to write this little script to find and
conver the kick-off times for the `Six
Nations <http://en.wikipedia.org/wiki/2015_Six_Nations_Championship>`__
automatically. It's quite an easy exercise in web scraping and time
conversion.

.. code:: python

    # loading some necessary libraries
    import requests
    import arrow

    from tabulate import tabulate
    from bs4 import BeautifulSoup

I decided to scrape the data from the official website, as they had both
local and GMT times for each match. The presence of GMT times makes it a
lot easier to convert them to the Pacific time zone! The combination of
the `requests <http://docs.python-requests.org/en/latest/>`__ library
and `Beautiful Soup <http://www.crummy.com/software/BeautifulSoup/>`__
is well tested and gives us the HTML code of the website:

.. code:: python

    url = 'http://www.rbs6nations.com/en/matchcentre/fixtures_and_results.php'
    r = requests.get(url)
    soup = BeautifulSoup(r.content)

When it comes to webscraping, some snooping around in the HTML code is
always necessary to find the information you are interested in. Luckily,
the fixtures are simply listed in table, which each fixture in a table
row. These rows belong either to the class *odd
group\_tests\_sixnations* or *even group\_tests\_sixnations* and are
thus easy to extract with the *class\_* parameter:

.. code:: python

    fixtures = soup.findAll('tr', class_="odd group_tests_sixnations")
    fixtures2 = soup.findAll('tr', class_="even group_tests_sixnations")

Now, for each fixture in our two lists we can get some additional data:
the home and away team, and the date and time of kick-off. We are only
interested in matches that are in the future, so we can simply check for
that. The `arrow <http://crsmithdev.com/arrow/>`__ library comes in
handy to that. Python has a variety of libraries that deal with dates
and times, but for this purpose, *arrow* serves really well. At the end,
we store the data for each future fixture in a list.

.. code:: python

    today = arrow.now()
    all_fix = []
    for fix in fixtures+fixtures2:
        date = fix.find("td", class_ = "field_DateDmyLong").get_text()
        time = fix.find("td", class_ = "field_UTCTimeLong").get_text()
        d = arrow.get(date + " "+time, "DD/MM/YYYY HH:mm")
        d_c = d.to('US/Pacific')
        if d_c > today:
            home_team = fix.find("td", class_ = "field_HomeDisplay").get_text()
            away_team = fix.find("td", class_ = "field_AwayDisplay").get_text()
            all_fix.append((home_team, away_team, d_c))

The fixture list now looks a little messy, and is not sorted by date:

.. code:: python

    all_fix



.. parsed-literal::

    [(u'Scotland', u'Italy', <Arrow [2015-02-28T06:30:00-08:00]>),
     (u'Ireland', u'England', <Arrow [2015-03-01T07:00:00-08:00]>),
     (u'England', u'Scotland', <Arrow [2015-03-14T10:00:00-07:00]>),
     (u'Italy', u'Wales', <Arrow [2015-03-21T05:30:00-07:00]>),
     (u'England', u'France', <Arrow [2015-03-21T10:00:00-07:00]>),
     (u'France', u'Wales', <Arrow [2015-02-28T09:00:00-08:00]>),
     (u'Wales', u'Ireland', <Arrow [2015-03-14T07:30:00-07:00]>),
     (u'Italy', u'France', <Arrow [2015-03-15T08:00:00-07:00]>),
     (u'Scotland', u'Ireland', <Arrow [2015-03-21T07:30:00-07:00]>)]



Using a lambda expression, we can sort the fixture list by date. To make
the list easier to read by humans (aka me), we can split up the *arrow*
timestamp into a field for date and one for time. Using *tabulate* then
prints a prettier list.

.. code:: python

    all_fix_sorted = sorted(all_fix, key=lambda x: x[2])
    all_fix_sorted = map(lambda x: (x[0], x[1], x[2].format('MM/DD/YYYY'), x[2].format('HH:mm')), all_fix_sorted)

.. code:: python

    print tabulate(all_fix_sorted, headers=["Home", "Away", "Day", "Time"])

.. parsed-literal::

    Home      Away      Day         Time
    --------  --------  ----------  ------
    Scotland  Italy     02/28/2015  06:30
    France    Wales     02/28/2015  09:00
    Ireland   England   03/01/2015  07:00
    Wales     Ireland   03/14/2015  07:30
    England   Scotland  03/14/2015  10:00
    Italy     France    03/15/2015  08:00
    Italy     Wales     03/21/2015  05:30
    Scotland  Ireland   03/21/2015  07:30
    England   France    03/21/2015  10:00


There we have it. A nice list of the next fixtures in the 2015 Six
Nations! Of course, if this was not just for personal use, you could
tidy up the output a little more, but an ASCII table is more than enough
for me. It beats looking up times manually for sure!
