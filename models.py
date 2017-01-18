from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


PLAYER_NAME_LENGTH = 64
TOURNAMENT_NAME_LENGTH = 255


Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'

    # local
    id = Column(Integer, primary_key=True)
    name = Column(String(PLAYER_NAME_LENGTH), unique=True)

    # one -> many
    placements = relationship('Placement', back_populates='player')


class Game(Base):
    __tablename__ = 'games'

    # local
    id = Column(Integer, primary_key=True)
    stocks_remaining = Column(Integer, nullable=False)

    # many -> one
    winner_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    winner = relationship('Player', foreign_keys=[winner_id])
    loser_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    loser = relationship('Player', foreign_keys=[loser_id])

    set_id = Column(Integer, ForeignKey('sets.id'), nullable=True)
    set = relationship('Set', back_populates='games')

    tournament_id = Column(
            Integer,
            ForeignKey('tournaments.id'),
            nullable=False)
    tournament = relationship('Tournament', back_populates='games')


class Set(Base):
    __tablename__ = 'sets'

    id = Column(Integer, primary_key=True)

    # one -> many
    games = relationship('Game', back_populates='set')


class Tournament(Base):
    __tablename__ = 'tournaments'

    # local
    id = Column(Integer, primary_key=True)
    name = Column(String(TOURNAMENT_NAME_LENGTH), unique=True)
    start_date = Column(Date)
    end_date = Column(Date)

    # one -> many
    games = relationship('Game', back_populates='tournament')
    placements = relationship('Placement', back_populates='tournament')


class Placement(Base):
    __tablename__ = 'placements'

    # local
    id = Column(Integer, primary_key=True)
    place = Column(Integer, nullable=False)

    # many -> one
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    player = relationship('Player', back_populates='placements')

    tournament_id = Column(
        Integer,
        ForeignKey('tournaments.id'),
        nullable=False)
    tournament = relationship('Tournament', back_populates='placements')

