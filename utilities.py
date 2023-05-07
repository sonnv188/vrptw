import datetime
import time

class Utilities:
    def __init__(self):
        print('Utilities...')
    def DateTime2Int(self, dt):
        element = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        tuple = element.timetuple()
        timestamp = time.mktime(tuple)
        return timestamp

    def int2DateTime(self, dt):
        return datetime.fromtimestamp(dt)

    def removeSubTitle(self, s):
        if "fm-" in s:
            s = s.replace("fm-", "")
        if "lm-" in s:
            s = s.replace("lm-", "")
        if "as-" in s:
            s = s.replace("as-", "")
        if "fc-" in s:
            s = s.replace("fc-", "")
        if "hubhn" in s or "hub-hn5" in s:
            s = "hn5"
        if "hub-hn4" in s:
            s = "hn4"
        return s
