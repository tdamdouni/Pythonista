"""Datetime support for JSON en-/decoding.

Example usage::

    >>> dumps({'timestamp': datetime.datetime.now()})
    '{"timestamp": "2015-02-11T13:44:41.504885"}'

See also http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript/3235787#3235787

"""
import json
from datetime import date, datetime

class JSONDateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        return (obj.isoformat() if isinstance(obj, (date, datetime)) else
            json.JSONEncoder.default(self, obj))

def datetime_decoder(d):
    result = []
    for k,v in (enumerate(d) if isinstance(d, list) else d.items()):
        if isinstance(v, basestring):
            try:
                v = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                try:
                    v = datetime.strptime(v, '%Y-%m-%d').date()
                except ValueError: pass
        elif isinstance(v, (dict, list)):
            v = datetime_decoder(v)
        result.append((k, v))
    return [x[1] for x in result] if isinstance(d, list) else dict(result)

dumps = lambda obj: json.dumps(obj, cls=JSONDateTimeEncoder)
loads = lambda obj: json.loads(obj, object_hook=datetime_decoder)
