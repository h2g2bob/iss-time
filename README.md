Works out the time on the International Space Station, in "local time".

"Local time" here means the timezone of the country which the ISS is above.

In real life, the ISS uses UTC.

APIs
====

This uses the following (free) APIs:
* http://api.open-notify.org/
* http://api.timezonedb.com/

Setup
=====

Create sqlite3 database:
```
sqlite> CREATE TABLE datapoints (nowutc INTEGER, lat REAL, lng REAL, tzdata TEXT, issnow TEXT, description TEXT, tzabbr TEXT, country TEXT);
sqlite> CREATE INDEX idx_datapoints_utc ON datapoints(nowutc);
```

Usage
=====

Run this regularly:
```
python -m iss_time.fetch_and_store
```

Simple output page:
```
python -m iss_time.display
```
