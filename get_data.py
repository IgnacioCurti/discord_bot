import os
import requests
from dotenv import load_dotenv
from db import session
from db import Match, Team
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY")


COMPETITION_CODE = 'WC'
BASE_URI = 'https://api.football-data.org/v4'
headers = { 'X-Auth-Token': API_KEY, 'Accept-Encoding': '' }


def get_matches():
    uri = BASE_URI + '/competitions/' + COMPETITION_CODE + '/matches'
    response = requests.get(uri, headers=headers)
    matches = response.json()['matches']
    
    for match in matches:
        if session.query(Match).filter_by(match_id = match['id']).first():
            continue
        new_match = Match()
        new_match.match_id = match['id']
        new_match.home_team_id = match['homeTeam']['id']
        new_match.away_team_id = match['awayTeam']['id']
        datetime_object = datetime.fromisoformat(f'{match["utcDate"]}'[:-1])
        a = datetime.strftime(datetime_object, '%Y-%m-%d %H:%M:%S')
        new_match.utc_datetime = datetime_object
        new_match.fifa_group = match['group']
        new_match.home_score = match['score']['fullTime']['home']
        new_match.away_score = match['score']['fullTime']['away']
        new_match.match_day = match['matchday']
        new_match.stage = match['stage']
        session.add(new_match)
        session.commit()


def get_teams():
    uri = BASE_URI  + '/competitions/' + COMPETITION_CODE + '/teams'
    response = requests.get(uri, headers=headers)
    teams = response.json()['teams']


    for team in teams:
        if session.query(Team).filter_by(team_id = team['id']).first():
            continue
        new_team = Team()
        new_team.team_id = team['id']
        new_team.name = team['name']
        session.add(new_team)
        session.commit()


def update_match(match_id, home_score, away_score):
    session.query(Match).filter_by(match_id = match_id).update({
        'home_score': home_score,
        'away_score': away_score,
        'finished': True

    })
    session.commit()

# get_teams()
# get_matches()
# update_match(391893, 2, 0)