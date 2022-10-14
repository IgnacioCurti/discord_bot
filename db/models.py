from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.base import engine, Base


class Team(Base):
    __tablename__ = 'teams'

    team_id = Column(Integer, primary_key = True)
    name = Column(String(100))


class Match(Base):
    __tablename__ = 'matches'

    match_id = Column(Integer, primary_key = True)
    fifa_group = Column(String(10))
    home_team_id = Column(Integer, ForeignKey(Team.team_id))
    away_team_id = Column(Integer, ForeignKey(Team.team_id))
    home_score = Column(Integer, default = 0)
    away_score = Column(Integer, default = 0)
    utc_datetime = Column(DateTime(timezone=False))
    match_day = Column(Integer)
    stage = Column(String(25))
    finished = Column(Boolean, default = False)

    home_team = relationship("Team", primaryjoin = "Team.team_id == Match.home_team_id", backref="matches_home", uselist = False, lazy='joined')
    away_team = relationship("Team", primaryjoin = "Team.team_id == Match.away_team_id", backref="matches_away", uselist = False, lazy='joined')


Base.metadata.create_all(engine)