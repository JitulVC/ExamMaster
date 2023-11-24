from flask import Flask

from Extension import db,ma

class Privilege(db.Model):
    __tablename__ = 'privileges'

    id = db.Column(db.Integer, primary_key=True)
    privileges = db.Column(db.String(40), unique=False, nullable=False)
    rec_insertedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    rec_lastupdatedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

class PrivilegeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Privilege
        load_instance = True
        ordered = True
