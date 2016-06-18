"""
What time is it on the ISS?
"""

from __future__ import print_function

import datetime
import json
import logging
import pytz
import sqlite3
import time
import urllib2

from .constants import ISS_TIME_DB
from .secrets import TIMEZONEDB_KEY


def fetch_iss_location():
	# {u'timestamp': 1466254762, u'message': u'success', u'iss_position': {u'latitude': -48.58972669884976, u'longitude': -114.65637752138807}}
	f = urllib2.urlopen('http://api.open-notify.org/iss-now.json')
	data = json.load(f)
	lat = data['iss_position']['latitude']
	lng = data['iss_position']['longitude']
	return (lat, lng)

def fetch_timezone(lat, lng):
	loc = 'http://api.timezonedb.com/v2/get-time-zone?key={key}&format=json&by=position&lat={lat:.6f}&lng={lng:.6f}'.format(
		key=TIMEZONEDB_KEY,
		lat=lat,
		lng=lng)
	f = urllib2.urlopen(loc)
	data = json.load(f)
	return data

def calculated_datetime(tzdata):
	try:
		timezone = pytz.timezone(tzdata[u'zoneName'])
		zone_name_long = tzdata[u'zoneName']
	except Exception:
		timezone = pytz.utc
		zone_name_long = 'UTC (error)'

	message = tzdata[u'message']
	if message:
		zone_name_long += ' - ' + message

	now = datetime.datetime.now(timezone)
	return (now, zone_name_long)

def fetch_data():
	lat, lng = fetch_iss_location()
	logging.debug('ll=%r, %r', lat, lng)

	tzdata = fetch_timezone(lat, lng)
	logging.debug('tzdata=%r', tzdata)

	issnow, description = calculated_datetime(tzdata)
	logging.debug('issnow=%r desc=%r', issnow, description)

	return (lat, lng, tzdata, issnow, description)


def store_data(lat, lng, tzdata, issnow, description):
	tzabbr = tzdata[u'abbreviation']
	country = tzdata[u'countryName']

	nowutc = time.time()

	conn = sqlite3.connect(ISS_TIME_DB)
	try:
		conn.execute('INSERT INTO datapoints(nowutc, lat, lng, tzdata, issnow, description, tzabbr, country) VALUES (?, ?, ?, ?, ?, ?, ?, ?);',
			(int(nowutc), lat, lng, json.dumps(tzdata), issnow, description, tzabbr, country))
		conn.commit()
	finally:
		conn.close()

def fetch_and_store():
	data = fetch_data()
	store_data(*data)

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	fetch_and_store()
