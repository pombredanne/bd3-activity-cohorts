from itertools import groupby
from datetime import datetime
from bitdeli.model import model
        
def day(hours):
    for hour, count in hours:
        yield datetime.utcfromtimestamp(hour * 3600).strftime('%Y%m%d')
        
@model
def build(profiles):
    for profile in profiles:
        uid = profile.uid
        for event, hours in profile['events'].iteritems():
            for date, counts in groupby(day(hours)):
                yield '%s:%s' % (date, event), uid