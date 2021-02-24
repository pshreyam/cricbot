''' Score provider for our bot

This module returns the list of fixtures and recent cricket matches.
'''

import os
from datetime import datetime

import cricapi
import dateutil.parser as dp
from dotenv import load_dotenv

load_dotenv()

cricapi = cricapi.Cricapi(os.getenv('CRICAPI_KEY'))

def format_date(date):
    ''' Format date for quick calculation '''

    split_date = date.split()
    split_date[1] = split_date[1][:3]
    return datetime.strptime(' '.join(split_date), '%d %b %Y')

def get_fixtures():
    ''' Get the fixtures for 7 days time '''

    fixtures = []

    for x in cricapi.matchCalendar()['data']:
        if abs((format_date(x['date']) - datetime.utcnow()).days) <= 7:
            fixtures.append({
                'name': x['name'],
                'date': x['date']
            })

    return fixtures

def get_results():
    ''' Get the recently concluded or ongoing matches '''

    results = []

    for x in cricapi.matches()['matches']:
        if x['matchStarted'] == True:
            current_utc_time = datetime.utcnow()
            match_utc_time = dp.parse(x['dateTimeGMT']).replace(tzinfo=None)

            if abs((current_utc_time - match_utc_time).days) <= 1.5:
                formatted_data = {
                    'id': x['unique_id'],
                    'game': f'[{x["unique_id"]}] {x["team-1"]} vs {x["team-2"]}',
                    'utc_date': match_utc_time.strftime('%m/%d/%Y, %-H:%M')
                }

                if 'toss_winner_team' in x.keys():
                    formatted_data['game'] += f' (toss: {x["toss_winner_team"]})'

                if 'winner_team' in x.keys():
                    formatted_data['game'] += f' (winner: {x["winner_team"]})'

                results.append(formatted_data)

    return results

def get_score(match_id):
    ''' Get the score for a requested match '''

    try:
        return cricapi.cricketScore({'unique_id': match_id})['score']
    except:
        return 'Sorry! match not found or error detected!'