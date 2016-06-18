"""
What time is it on the ISS?
"""

from __future__ import print_function

import urllib2
import json

# You can register api access for free at https://timezonedb.com/register
from .secret import TIMEZONEDB_KEY

def fetch_iss_location():
	# {u'timestamp': 1466254762, u'message': u'success', u'iss_position': {u'latitude': -48.58972669884976, u'longitude': -114.65637752138807}}
	f = urllib2.urlopen('http://api.open-notify.org/iss-now.json')
	data = json.load(f)
	lat = data['iss_position']['latitude']
	lng = data['iss_position']['longitude']
	return (lat, lng)

def fetch_timezone(lat, lng):
	f = urllib.urlopen('http://api.timezonedb.com/v2/get-time-zone?key={key}&format=json&by=position&lat={lat:.6f}&long={lng:.6f}'.format(
		key=TIMEZONEDB_KEY,
		lat=lat,
		lng=lng))
	data = json.load(f)
	return data

def main():
	lat, lng = fetch_iss_location()
	data = fetch_timezone(lat, lng)
	print(data)
