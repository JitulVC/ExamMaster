from flask import Flask

from Extension import db,ma

class StudentExam(db.Model):
    __tablename__ = 'studentexams'

    id = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.Integer, nullable=False)
    examid = db.Column(db.Integer, nullable=False)
    attemptno = db.Column(db.Integer, nullable=False)
    examscore = db.Column(db.Integer, nullable=False)
    starttime = db.Column(db.DateTime(), nullable=False)
    endtime = db.Column(db.DateTime(), nullable=False)
    rec_insertedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    rec_lastupdatedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

class StudentExamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentExam
        load_instance = True
        ordered = True
