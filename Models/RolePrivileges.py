from flask import Flask

from Extension import db,ma

class RolePrivilege(db.Model):
    __tablename__ = 'roleprivileges'

    id = db.Column(db.Integer, primary_key=True)
    roleid = db.Column(db.Integer, nullable=False)
    privilegeid = db.Column(db.Integer, nullable=False)
    rec_insertedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    rec_lastupdatedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

class RolePrivilegeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RolePrivilege
        load_instance = True
        ordered = True
