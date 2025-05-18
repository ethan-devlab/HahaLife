# import pytz
from datetime import datetime, timezone
from tzlocal import get_localzone
import pytz

utc_dt = datetime.now(timezone.utc)

local_tz = get_localzone()

print("Local Time:", utc_dt.astimezone(local_tz))

TPE = pytz.timezone('Asia/Taipei')
print("Taipei Time:", utc_dt.astimezone(TPE))

created_at = datetime.now().astimezone(TPE).strftime('%Y-%m-%d %H:%M:%S')
print(f"Local timezone: {local_tz}")
print("Created At:", created_at)