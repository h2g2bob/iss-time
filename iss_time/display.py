from __future__ import print_function
from __future__ import unicode_literals

import sqlite3

from .constants import ISS_TIME_DB


def get_most_recent():
	conn = sqlite3.connect(ISS_TIME_DB)
	try:
		[row] = conn.execute('SELECT nowutc, lat, lng, tzdata, issnow, description, tzabbr, country FROM datapoints ORDER BY nowutc DESC LIMIT 1;')
		return row
	finally:
		conn.close()


def main():
	_nowutc, _lat, _lng, _tzdata, issnow, _description, _tzabbr, country = get_most_recent()
	print('Time on space station is: {issnow} ({country})'.format(
		issnow=issnow,
		country=country))

if __name__ == '__main__':
	main()
