from datetime import datetime, timedelta
from db import Match
from db import session


def get_matches_by_date(date):
    if not date:
        fromDate = datetime.today()
    else:
        fromDate = datetime.strptime(date, '%Y-%m-%d')
    toDate = fromDate + timedelta(days=1)
    matches = session.query(Match).filter(Match.utc_datetime >= fromDate, Match.utc_datetime < toDate).all()
    message = f"Partidos del {date}:"
    if len(matches) == 0:
        return f'No hay partidos para esa fecha. Si crees que es un error revisa el formato de fecha. Recuerda que el formato de fecha es "AAAA/MM/DD".'
    else:
        for match in matches:
            home_team = match.home_team.name if match.home_team else "To Be Determined"
            away_team = match.away_team.name if match.away_team else "To Be Determined"
            if match.finished:
                home_team = f"{home_team} {match.home_score}"
                away_team = f"{match.away_score} {away_team}"
                separator = " - "
                time = "TERMINADO"
            else:
                separator = " VS "
                time = " a las " + (match.utc_datetime - timedelta(hours=3)).strftime("%H:%M")
            phase = match.fifa_group + " Jornada " + str(match.match_day) + ": " if match.match_day else match.stage + ": "
            message = message + "\n" + phase + home_team + separator + away_team + time
        return message
        


