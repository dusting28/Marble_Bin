from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from os import path

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(150))
    Password = db.Column(db.String(150))
    notes = db.relationship('Note')

class TournamentResult(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Marble_ID = db.Column(db.Integer, db.ForeignKey('marble.ID')) #Maybe lowercase ID
    Tournament_ID = db.Column(db.Integer, db.ForeignKey('big_tournament.ID'))
    Team = db.Column(db.String(1))
    Group = db.Column(db.String(1))
    Race1 = db.Column(db.Integer)
    Race2 = db.Column(db.Integer)
    Race3 = db.Column(db.Integer)
    Race4 = db.Column(db.Integer)
    Group_Winner = db.Column(db.Boolean)
    Group_RunnerUp = db.Column(db.Boolean)
    Top12 = db.Column(db.Integer)

class Marble(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(30), default = "New Marble", unique=True)
    Team = db.Column(db.String(1), default = "I")
    Cheat = db.Column(db.Boolean, default = False)
    Weight = db.Column(db.Integer, default = 4500)
    Diameter1 = db.Column(db.Integer, default = 600)
    Diameter2 = db.Column(db.Integer, default = 600)
    Image = db.Column(db.String(50), default = "EMPTY.png")
    Time_Trials = db.Column(db.String(50), default = "EMPTY.csv")
    Results = db.relationship('TournamentResult')

class BigTournament(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    List_Num = db.Column(db.Integer)
    Tournament_Num = db.Column(db.Integer)
    Results = db.relationship('TournamentResult')