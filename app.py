import os
from flask import Flask, request,send_file
from pytz import UTC # timezone
from dataclasses import dataclass
from lib import get_events_by_leagues_and_teams, get_calendar_buffer

if os.getenv('ESPORTS_TOKEN') is None:
    raise("empty token")

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static')

@app.route('/')
def root():
    return app.send_static_file("index.html")

@app.route('/calendar', methods=['GET'])
def calendar():
    leagues = [x.lower() for x in request.args.get('leagues', '').split(',')]
    fav_teams = [x.upper() for x in request.args.get('teams','').split(',') if x != '']
    print(leagues, fav_teams)
    events = get_events_by_leagues_and_teams(leagues, fav_teams)
    name = '-'.join(leagues)+'-'.join(fav_teams)
    return send_file(get_calendar_buffer(name, events), as_attachment=True,
                     attachment_filename=f'{name}.ics',
                     mimetype='text/ics')
