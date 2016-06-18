from __future__ import print_function
from __future__ import unicode_literals

import sqlite3
import time

from .constants import ISS_TIME_DB


def get_most_recent(limit):
	conn = sqlite3.connect(ISS_TIME_DB)
	try:
		rows = conn.execute('SELECT nowutc, lat, lng, tzdata, issnow, description, tzabbr, country FROM datapoints ORDER BY nowutc DESC LIMIT ?;', (limit,))
		return list(rows)
	finally:
		conn.close()


def main():
	for nowutc, _lat, _lng, _tzdata, issnow, _description, _tzabbr, country in get_most_recent(120):
		print('At {nowutc}, time on space station is: {issnow} ({country})'.format(
			nowutc=time.ctime(nowutc),
			issnow=issnow,
			country=country))

if __name__ == '__main__':
	main()
