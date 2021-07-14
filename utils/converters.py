# Importing time modules
from datetime import datetime, timedelta

def getest():
    delta = timedelta(hours=4)
    Time = datetime.utcnow() - delta # Subtracting 4 hours from UTC time, so the returned time will be in EST.
    return Time.strftime("%a, %d %b %Y @ %I:%M:%S %p EST") # Example: returns 'Wed, 14 Jul 2021 @ 3:59:06 PM EST'
