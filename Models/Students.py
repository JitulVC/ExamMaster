from flask import Flask

from Extension import db,ma

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    studentname = db.Column(db.String(50), unique=False, nullable=False)
    userid = db.Column(db.Integer, nullable=False)
    lastlogin = db.Column(db.DateTime(), nullable=True)
    rec_insertedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    rec_lastupdatedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        ordered = True
