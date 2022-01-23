import json
from typing import List
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from dateutil import parser
from pytz import UTC # timezone
from dataclasses import dataclass
import requests

import requests
from lib import get_events_by_leagues_and_teams, get_calendar_buffer

if __name__ == "__main__":
    events = get_events_by_leagues_and_teams(['lec'],[])
    buffer = get_calendar_buffer("lec", events)
    with open("lec.ics", "wb") as f:
        f.write(buffer.getbuffer())
        f.close()
    