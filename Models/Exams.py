from flask import Flask

from Extension import db,ma

class Exam(db.Model):
    __tablename__ = 'exams'

    id = db.Column(db.Integer, primary_key=True)
    examname = db.Column(db.String(60), unique=False, nullable=False)
    no_of_questions = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    totalscore = db.Column(db.Integer, nullable=False)
    passingscore = db.Column(db.Integer, nullable=False)
    rec_insertedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    rec_lastupdatedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

class ExamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exam
        load_instance = True
        ordered = True
