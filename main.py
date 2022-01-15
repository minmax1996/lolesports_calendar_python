import json
from typing import List
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from dateutil import parser
from pytz import UTC # timezone
from dataclasses import dataclass
import requests


league_ids = {
    "lec": "98767991302996019",
    "lcl": "98767991355908944",
    "lcs": "98767991299243165"
}

def get_events_from_api(leagues: List[str]):
    events = []
    next_page = ""
    while next_page != None:
        print(next_page)
        try:
            resp = fetch_schedule(leagues, next_page)
        except Exception as exp:
            print(exp)
            break

        events += resp["data"]["schedule"]["events"]
        next_page = resp["data"]["schedule"]["pages"]["newer"]

    return events

def fetch_schedule(leagues: List[str], page_token: str = ""):
    url = "https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=en-GB&" + \
    f"&leagueId={str.join(',',[league_ids[x] for x in leagues])}" + \
    (f"&pageToken={page_token}" if page_token != "" else "")

    payload={}
    headers = {
        'authority': 'esports-api.lolesports.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'x-api-key': '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z',
        'sec-ch-ua-platform': '"macOS"',
        'accept': '*/*',
        'origin': 'https://lolesports.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://lolesports.com/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        raise Exception(f"status code: {response.status_code}", response.text)
    return json.loads(response.text)

@dataclass
class LolEvent:
    id: str
    league_name: str
    week_name: str
    start_time: str
    t1: str
    t2: str
    has_vod: bool

def save_to_calendar(name, events):
    cal = Calendar()
    cal.add('prodid', f'-//{name}//mxm.dk//')
    cal.add('version', '2.0')

    for e in events:
        event = Event()
        start_date = parser.parse(e.start_time)
        event.add('summary', f'{e.league_name} {e.week_name}: {e.t1} vs {e.t2}')
        event.add('dtstart', start_date)
        event.add('dtend', start_date +  timedelta(hours=1))
        event.add('dtstamp', datetime.now())

        if e.has_vod:
            event.add('description', f'game completed: find vod here: https://lolesports.com/vod/{e.id}/1/')
        else:
            event.add('description', f'join live here: https://lolesports.com/live/{e.league_name.lower()}/{e.league_name.lower()}/')
        
        event['uid'] = f'{e.id}'
        event.add('priority', 5)
        cal.add_component(event)

    f = open(f'{name}.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

if __name__ == "__main__":
    fav_teams = []
    response = get_events_from_api(["lcs"])
    cal_events = []
    for e in response:
        if e["type"] == "match":
            le = LolEvent(
                e["match"]["id"],
                e["league"]["name"],
                e["blockName"],
                e["startTime"],
                e["match"]["teams"][0]["code"],
                e["match"]["teams"][1]["code"],
                "hasVod" in e["match"]["flags"])
                
            #skip match if fav teams defined and match dont contains fav team
            if len(fav_teams) > 0 and le.t1 not in fav_teams and le.t2 not in fav_teams:
                continue

            print(le, e["state"], len(fav_teams) > 0,  le.t1 not in fav_teams, le.t2 not in fav_teams)
            cal_events.append(le)

    save_to_calendar("lcs", cal_events)
    