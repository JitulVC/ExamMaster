from flask import Flask

from Extension import db,ma

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    useraccount = db.Column(db.String(40), unique=False, nullable=False)
    username = db.Column(db.String(60), unique=False, nullable=False)
    passcode = db.Column(db.String(200), unique=False, nullable=False)
    roleid = db.Column(db.Integer, nullable=False)
    apikey = db.Column(db.String(100), nullable=True)
    rec_insertedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    rec_lastupdatedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        ordered = True
