from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from os import path

class Team(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Ticker = db.Column(db.String(1), default = " ")
    Slots = db.Column(db.Integer, default = 12)
    MascotSlots = db.Column(db.Integer, default = 1)
    Money = db.Column(db.Integer, default = 0)
    Points = db.Column(db.Integer, default = 0)
    ColorR = db.Column(db.Integer, default=255)
    ColorG = db.Column(db.Integer, default=255)
    ColorB = db.Column(db.Integer, default=255) 

class Marble(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(30), default = "New Marble", unique=True)
    Team = db.Column(db.String(1), default = "I")
    TeamPosition = db.Column(db.Integer, default = 16)
    Cheat = db.Column(db.Boolean, default = False)
    Weight = db.Column(db.Integer, default = 4500)
    Diameter1 = db.Column(db.Integer, default = 600)
    Diameter2 = db.Column(db.Integer, default = 600)
    Image = db.Column(db.String(50), default = "EMPTY.png")
    Time_Trials = db.Column(db.String(50), default = "EMPTY.csv")
    TournamentResult = db.relationship('TournamentResult', backref='marble')
    Transaction = db.relationship('Transaction', backref='marble')
    Rating = db.relationship('Rating', backref='marble')

class TournamentResult(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Marble_ID = db.Column(db.Integer, db.ForeignKey('marble.ID')) # Maybe lowercase ID
    Tournament_ID = db.Column(db.Integer, db.ForeignKey('big_tournament.ID'))
    Team = db.Column(db.String(1))
    Group = db.Column(db.String(1))
    Group_Row = db.Column(db.Integer)
    Race1 = db.Column(db.Integer) # 4 = Unknown
    Race2 = db.Column(db.Integer)
    Race3 = db.Column(db.Integer)
    Race4 = db.Column(db.Integer)
    Group_Pos = db.Column(db.String(1)) # 1 = Winner, 2 = Runner Up, - = Eliminated, Space = Unkown 
    OnevOne = db.Column(db.String(1)) # Number = Number of Points, + = Advanced, - = Eliminated, Space = Unkown
    Top12 = db.Column(db.Integer) #0 - Unknown, -1 - Not Podium

class BigTournament(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    List_Num = db.Column(db.Integer)
    Tournament_Num = db.Column(db.Integer)
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    List_ID = db.Column(db.Integer, db.ForeignKey('list.ID'))
    Results = db.relationship('TournamentResult', backref='big_tournament')

class Transaction(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(30)) # Trade, Draft, Re-Entry Draft, Ithica Draft, Gift, Found, Discovered, Marble Money / Jar, Cheat, Reinstated, Kicked-Off, Pensioned, Lost
    OriginalTeam = db.Column(db.String(1))
    FinalTeam = db.Column(db.String(1))
    Unsigned = db.Column(db.Boolean, default = False)
    Money_Cost = db.Column(db.Integer, default = 0) # Money Gained by Original Team
    Points_Cost = db.Column(db.Integer, default = 0) # Draft Points Gained by Original Team
    Pick_Number = db.Column(db.Integer, default = 0) # Draft Points Gained by Original Team
    Roster_Slot = db.Column(db.Boolean, default = False)
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    Loan = db.Column(db.Boolean, default = False)
    LoanEndDate = db.Column(db.DateTime(timezone=True), default=func.now())
    Marble_ID = db.Column(db.Integer, db.ForeignKey('marble.ID')) # Maybe lowercase ID?
    Trade_ID = db.Column(db.Integer, db.ForeignKey('trade.ID')) # Maybe lowercase ID?
    Draft_ID = db.Column(db.Integer, db.ForeignKey('draft.ID')) # Maybe lowercase ID?

class Trade(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    Transactions = db.relationship('Transaction', backref='trade')

class Draft(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20))
    Type = db.Column(db.String(20)) # Classic, Draft Points, Marble Money, Draft Point Run-Off
    FindersBonus = db.Column(db.Boolean, default = False)
    SnakeDraft = db.Column(db.Boolean, default = False)
    TeamROrder = db.Column(db.Integer, default = 0)
    TeamUOrder = db.Column(db.Integer, default = 0)
    TeamJOrder = db.Column(db.Integer, default = 0)
    TeamAOrder = db.Column(db.Integer, default = 0)
    TeamRPoints = db.Column(db.Integer, default = 0)
    TeamUPoints = db.Column(db.Integer, default = 0)
    TeamJPoints = db.Column(db.Integer, default = 0)
    TeamAPoints = db.Column(db.Integer, default = 0)
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    Picks = db.relationship('Transaction', backref='draft')

class Rating(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Team = db.Column(db.String(1))
    Position = db.Column(db.Integer)
    TotalRating = db.Column(db.Integer)
    Marble_ID = db.Column(db.Integer, db.ForeignKey('marble.ID')) # Maybe lowercase ID
    List_ID = db.Column(db.Integer, db.ForeignKey('list.ID'))

class List(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    List_Num = db.Column(db.Integer)
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    BigTournament = db.relationship('BigTournament', backref='list')
    Rating = db.relationship('Rating', backref='list')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(150), unique=True)
    Password = db.Column(db.String(150))
