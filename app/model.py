from . import db

class player(db.Model):
    __tablename__='player'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    age=db.Column(db.Integer)
    nationality= db.Column(db.String(255))
    height=db.Column(db.Integer)