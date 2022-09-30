import json
import os
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
    if os.getenv('ESPORTS_TOKEN') is None:
        raise("empty token")

    events = get_events_by_leagues_and_teams(['worlds'],[])
    buffer = get_calendar_buffer("worlds", events)
    with open("worlds.ics", "wb") as f:
        f.write(buffer.getbuffer())
        f.close()
    