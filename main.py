from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

# First Time

engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/sanitas_resort', echo=True)
Base = declarative_base()

# -----------------------------
# Tables
# -----------------------------

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    score = Column(Integer, default=0)  # Score total de l'équipe
    players = relationship("Player", back_populates="team")

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(String(20), default='en cours')  # en cours, terminé, perdu
    players = relationship("Player", back_populates="game")

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False)  # medecin, guide, analyste, coordinateur
    current_zone = Column(String(50), nullable=True)
    score = Column(Integer, default=0)  # Score individuel
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship("Team", back_populates="players")
    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship("Game", back_populates="players")
    actions = relationship("Action", back_populates="player")

class Zone(Base):
    __tablename__ = 'zones'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    is_quarantined = Column(Boolean, default=False)
    patients = relationship("Patient", back_populates="zone")

class Symptom(Base):
    __tablename__ = 'symptoms'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    severity = Column(Integer, nullable=False)  # 1 = léger, 5 = grave

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    zone_id = Column(Integer, ForeignKey('zones.id'))
    infected = Column(Boolean, default=False)
    zone = relationship("Zone", back_populates="patients")

class Action(Base):
    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    action_type = Column(String(50))  # ex: analyser, déplacer, communiquer
    target = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    player = relationship("Player", back_populates="actions")

# -----------------------------
# Création des tables
# -----------------------------
Base.metadata.create_all(engine)

# -----------------------------
# Exemple d'utilisation
# -----------------------------
Session = sessionmaker(bind=engine)
session = Session()

# Créer une équipe
team1 = Team(name="Equipe Alpha")
team2 = Team(name="Equipe Beta")
session.add_all([team1, team2])
session.commit()

# Créer une partie
game1 = Game()
session.add(game1)
session.commit()

# Ajouter des joueurs dans les équipes
player1 = Player(username='Alice', role='medecin', game=game1, team=team1)
player2 = Player(username='Bob', role='guide', game=game1, team=team1)
player3 = Player(username='Charlie', role='analyste', game=game1, team=team2)
player4 = Player(username='Diana', role='coordinateur', game=game1, team=team2)
session.add_all([player1, player2, player3, player4])
session.commit()

# Ajouter des zones
zone1 = Zone(name='Piscine')
zone2 = Zone(name='Restaurant')
session.add_all([zone1, zone2])
session.commit()

# Ajouter des patients
patient1 = Patient(name='Touriste1', zone=zone1, infected=True)
patient2 = Patient(name='Touriste2', zone=zone2, infected=False)
session.add_all([patient1, patient2])
session.commit()

print("Base de données avec équipes et rôles initialisée avec succès !")
