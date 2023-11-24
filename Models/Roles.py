from flask import Flask

from Extension import db,ma

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(40), unique=False, nullable=False)
    rec_insertedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    rec_lastupdatedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True
        ordered = True
