from datetime import datetime
from dateutil import tz


def get_time(time):
    event_time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')

    string_date = event_time.strftime('%Y-%m-%d %H:%M:%S')

    # Auto-detect time zones
    from_zone = tz.tzutc()
    to_zone = tz.gettz('America/Chicago')

    utc = datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S')

    # Tell the datetime object that it's in UTC time zone since datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=from_zone)

    # Convert to zone
    tz_time = utc.astimezone(to_zone).time()

    return tz_time

