# Author: Derek Kruszewski
# Code referenced from: Iowa State University (https://github.com/akrherz/iem/blob/master/scripts/asos/iem_scraper_example.py)
# Date: 2020-03-01

"""This script downloads weather data from 2013-01-01 to present day for Ohare Airport via Iowa State University Iowa Environmental Mesonet

Usage: download_weather.py
"""

import json
import time
import datetime
from urllib.request import urlopen

# Number of attempts to download data
MAX_ATTEMPTS = 6
# HTTPS here can be problematic for installs that don't have Lets Encrypt CA
SERVICE = "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"

def download_data(uri):
    """Fetch the data from the IEM
    The IEM download service has some protections in place to keep the number
    of inbound requests in check.  This function implements an exponential
    backoff to keep individual downloads from erroring.
    Args:
      uri (string): URL to fetch
    Returns:
      string data
    """
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        try:
            data = urlopen(uri, timeout=300).read().decode("utf-8")
            if data is not None and not data.startswith("ERROR"):
                return data
        except Exception as exp:
            print("download_data(%s) failed with %s" % (uri, exp))
            time.sleep(5)
        attempt += 1

    print("Exhausted attempts to download, returning empty data")
    return ""

def main():
    """Our main method"""
    
    # timestamps in UTC to request data for
    now = datetime.datetime.now()
    startts = datetime.datetime(2013, 1, 1)
    endts = datetime.datetime(now.year, now.month, now.day)

    service = SERVICE + "data=all&tz=Etc/UTC&format=comma&latlon=yes&"
    service += startts.strftime("year1=%Y&month1=%m&day1=%d&")
    service += endts.strftime("year2=%Y&month2=%m&day2=%d&")

    stations = ['ORD']
    for station in stations:
        uri = "%s&station=%s" % (service, station)
        print("Downloading: %s" % (station,))
        data = download_data(uri)
        outfn = "../data/ORD_weather.txt"
        out = open(outfn, "w")
        out.write(data)
        out.close()

# script entry point
if __name__ == '__main__':
    main()